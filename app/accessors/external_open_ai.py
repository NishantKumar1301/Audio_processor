from openai import OpenAI # type: ignore
import os
from dotenv import load_dotenv # type: ignore
load_dotenv()

class OpenAIAnalysisService:
    @staticmethod
    def extract_details_from_text(transcription):
        """
        Sends transcribed text to OpenAI and extracts selling price, product name, and cost price.
        :param transcription: Text to analyze
        :return: Dictionary with extracted details or an error message
        """
        client = OpenAI(api_key=os.getenv("API_KEY"))
        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a helpful assistant for analyzing transcriptions. "
                        "The transcription comes from audio processed using Whisper, "
                        "which might contain errors in mixed languages (Hindi, English, or Hinglish). "
                        "It will be in format like first selling price then product name then cost price. "
                        "Your task is to extract the following details in JSON format: "
                        "1. Selling Price (as a numeric value). "
                        "2. Product Name (as text). "
                        "3. Cost Price (as a numeric value)."
                    )
                },
                {
                    "role": "user",
                    "content": f"Analyze the transcription and extract details:\n{transcription}"
                }
            ],
            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "transaction_details",
                    "schema": {
                        "type": "object",
                        "properties": {
                            "selling_price": {
                                "description": "The selling price extracted from the transcription",
                                "type": ["number", "null"]
                            },
                            "product_name": {
                                "description": "The product name extracted from the transcription",
                                "type": ["string", "null"]
                            },
                            "cost_price": {
                                "description": "The cost price extracted from the transcription",
                                "type": ["number", "null"]
                            }
                        },
                        "required": ["selling_price", "product_name", "cost_price"],
                        "additionalProperties": False
                    }
                }
            }
        )

        try:
            print(response)
            return response.choices[0].message.content  # Return the structured JSON response
        except KeyError as e:
            return {"error": f"Missing key in response: {str(e)}"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
