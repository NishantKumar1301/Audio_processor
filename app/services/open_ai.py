from app.accessors.external_open_ai import OpenAIAnalysisService
from app.accessors.open_ai_request_log import OpenAIRequestLogAccessor
from app.accessors.transaction import TransactionAccessor
import json


class OpenAIService:
    @staticmethod
    def initialize_openai_requests():
        OpenAIRequestLogAccessor.create_initial_entries_for_openai_request()

    @staticmethod
    def process_pending_requests_and_create_transactions():
        """
        Process all PENDING OpenAIRequestLog entries:
        - Extract details using OpenAIAnalysisService.
        - Update request log with response and status.
        - Create or update corresponding Transaction entries.
        """
        pending_requests = OpenAIRequestLogAccessor.get_pending_requests()

        # Exit early if no pending requests
        if not pending_requests.exists():
            return

        for request_log in pending_requests:
            try:
                # Prepare request data
                transcription = request_log.audio_record.transcription
                request_data = transcription

                # Call OpenAI to extract details
                response_data = OpenAIAnalysisService.extract_details_from_text(transcription)
                print(f"Response data: {response_data}")

                # Determine status based on response
                status = "SUCCESS" if "error" not in response_data else "FAILED"

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
                    response_data_dict = json.loads(json.dumps(response_data)) if isinstance(response_data, dict) else json.loads(response_data)

                    TransactionAccessor.create_or_update_transaction(
                        openai_request=request_log,
                        product_name=response_data_dict.get("product_name"),
                        selling_price=response_data_dict.get("selling_price"),
                        cost_price=response_data_dict.get("cost_price"),
                    )

            except Exception as e:
                # Handle unexpected errors and mark as FAILED
                OpenAIRequestLogAccessor.update_request_log_status(
                    request_log=request_log,
                    request_data="",
                    response_data=str(e),
                    status="FAILED"
                )
