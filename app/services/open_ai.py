import logging
import json
from app.accessors.external_open_ai import OpenAIAnalysisService
from app.accessors.open_ai_request_log import OpenAIRequestLogAccessor
from app.accessors.transaction import TransactionAccessor

# Get the logger for the app
logger = logging.getLogger('app')

class OpenAIService:
    @staticmethod
    def initialize_openai_requests(user):
        """Creates initial OpenAI request logs for unprocessed audio records."""
        try:
            logger.info("Initializing OpenAI request logs for user: %s", user.username)
            OpenAIRequestLogAccessor.create_initial_entries_for_openai_request(user)
            logger.info("OpenAI request logs initialized successfully.")
        except Exception as e:
            logger.error(f"Error initializing OpenAI request logs: {e}", exc_info=True)

    @staticmethod
    def process_pending_requests_and_create_transactions():
        """
        Process all PENDING OpenAIRequestLog entries:
        - Extract details using OpenAIAnalysisService.
        - Update request log with response and status.
        - Create or update corresponding Transaction entries.
        """
        logger.info("Fetching pending OpenAI request logs...")
        pending_requests = OpenAIRequestLogAccessor.get_pending_requests()

        # Exit early if no pending requests
        if not pending_requests.exists():
            logger.info("No pending OpenAI requests found. Exiting.")
            return

        for request_log in pending_requests:
            try:
                logger.info(f"Processing request log ID: {request_log.id}")

                # Get transcription from audio record
                transcription = request_log.audio_record.transcription
                if not transcription:
                    logger.warning(f"No transcription found for request log ID: {request_log.id}")
                    continue

                logger.debug(f"Request transcription: {transcription}")

                # Call OpenAI to extract details
                response_data = OpenAIAnalysisService.extract_details_from_text(transcription)
                logger.debug(f"Response data from OpenAI: {response_data}")

                # Ensure response_data is properly formatted JSON
                try:
                    if isinstance(response_data, str):
                        response_data_dict = json.loads(response_data)
                    elif isinstance(response_data, dict):
                        response_data_dict = response_data
                    else:
                        raise ValueError("Unexpected response format from OpenAI")
                except json.JSONDecodeError as e:
                    logger.error(f"JSON decoding error for request log ID {request_log.id}: {e}")
                    response_data_dict = {"error": "Invalid OpenAI response format"}

                logger.info(f"Extracted Data for request log ID {request_log.id}: {response_data_dict}")

                # Determine request status
                status = "SUCCESS" if "error" not in response_data_dict else "FAILED"

                # Update OpenAIRequestLog entry
                OpenAIRequestLogAccessor.update_request_log_status(
                    request_log=request_log,
                    request_data=transcription,
                    response_data=json.dumps(response_data_dict),  # Store as JSON string
                    status=status
                )

                # If successful, create/update Transaction
                if status == "SUCCESS":
                    TransactionAccessor.create_or_update_transaction(
                        openai_request=request_log,
                        product_name=response_data_dict.get("product_name", "Unknown"),
                        selling_price=response_data_dict.get("selling_price", 0.00),
                        cost_price=response_data_dict.get("cost_price", 0.00),
                    )
                    logger.info(f"Transaction created/updated for request log ID {request_log.id}")
                else:
                    logger.warning(f"Request log ID {request_log.id} failed. Response: {response_data_dict}")

            except Exception as e:
                logger.error(f"Error processing request log ID {request_log.id}: {e}", exc_info=True)
                OpenAIRequestLogAccessor.update_request_log_status(
                    request_log=request_log,
                    request_data=transcription,
                    response_data=str(e),
                    status="FAILED"
                )
