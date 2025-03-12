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
        try:
            logger.info("Initializing OpenAI request logs.")
            # Pass the user to the accessor to create initial entries
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
        logger.info("Fetching pending OpenAI request logs.")
        pending_requests = OpenAIRequestLogAccessor.get_pending_requests()

        # Exit early if no pending requests
        if not pending_requests.exists():
            logger.info("No pending OpenAI requests found. Exiting.")
            return

        for request_log in pending_requests:
            try:
                logger.info(f"Processing request log ID: {request_log.id}")

                # Prepare request data
                transcription = request_log.audio_record.transcription
                request_data = transcription
                logger.debug(f"Request transcription: {transcription}")

                # Call OpenAI to extract details
                response_data = OpenAIAnalysisService.extract_details_from_text(transcription)
                logger.debug(f"Response data from OpenAI: {response_data}")

                # Determine status based on response
                status = "SUCCESS" if "error" not in response_data else "FAILED"
                logger.info(f"Request log ID {request_log.id} processed with status: {status}")

                # Update the OpenAIRequestLog entry
                OpenAIRequestLogAccessor.update_request_log_status(
                    request_log=request_log,
                    request_data=request_data,
                    response_data=json.dumps(response_data),  # Save response_data as JSON string
                    status=status
                )

                # If successful, create or update Transaction
                if status == "SUCCESS":
                    # Deserialize response_data before accessing
                    response_data_dict = (
                        json.loads(json.dumps(response_data)) if isinstance(response_data, dict) else json.loads(response_data)
                    )

                    TransactionAccessor.create_or_update_transaction(
                        openai_request=request_log,
                        product_name=response_data_dict.get("product_name"),
                        selling_price=response_data_dict.get("selling_price"),
                        cost_price=response_data_dict.get("cost_price"),
                    )
                    logger.info(f"Transaction created/updated for request log ID {request_log.id}")
                else:
                    logger.warning(f"Request log ID {request_log.id} failed with response: {response_data}")

            except Exception as e:
                # Handle unexpected errors and mark as FAILED
                logger.error(f"Error processing request log ID {request_log.id}: {e}", exc_info=True)
                OpenAIRequestLogAccessor.update_request_log_status(
                    request_log=request_log,
                    request_data="",
                    response_data=str(e),
                    status="FAILED"
                )
