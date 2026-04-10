import os
import logging
import argparse
from typing import List, Dict, Any
from groq import Groq
from dotenv import load_dotenv
#Imports
import csv_utils
import llm_client

#Logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def display_results(results: List[Dict[str, Any]]) -> None:
    """Prints a formatted summary report to the console."""
    print("\n" + "="*100)
    print(f"{'LEAD SUMMARIZATION REPORT':^100}")
    print("="*100)
    
    for i, row in enumerate(results, start=1):
        name = row.get("name", "Unknown").title()
        company = row.get("company", "Unknown").upper()
        email = row.get("email", "N/A")
        phone = row.get("phone", "N/A")
        summary = row.get("summary", "No summary available.")
        
        print(f"\n{i}. {name} @ {company}")
        print(f"   Contact: {email} | {phone}")
        print(f"   Summary: {summary}")
        print("-" * 50)
    
    print("="*100)
    print(f"{'END OF REPORT':^100}")
    print("="*100 + "\n")

def main(input_path: str, output_path: str) -> None:
    """Orchestrates the modular lead summarization process."""
    
    # 0.Load Secrets
    load_dotenv()
    api_key = os.environ.get("GROQ_API_KEY")
    model = os.environ.get("MODEL", "llama-3.3-70b-versatile")

    # 1.Pre-run check
    if not api_key:
        logger.error("Missing GROQ_API_KEY in .env file.")
        return

    if not os.path.exists(input_path):
        logger.error(f"Input file not found: {input_path}")
        return

    try:
        with open(output_path, "a", encoding="utf-8"):
            pass
    except (PermissionError, IOError):
        logger.error(f"Cannot write to output file: {output_path}. Please close it if open in Excel.")
        return

    # 2. File Validation

    if csv_utils.is_binary_file(input_path):
        logger.error(f"'{input_path}' appears to be binary. Please save as CSV.")
        return

    # 3. Detect settings and read
    encoding, delimiter = csv_utils.detect_csv_settings(input_path)
    if not encoding:
        logger.error(f"Could not decode {input_path}.")
        return

    logger.info(f"Processing leads from {input_path}...")
    
    # 4. Process Leads
    client = Groq(api_key=api_key)
    processed_results = []
    for row in csv_utils.read_csv_rows(input_path, encoding, delimiter):
        summary = llm_client.summarize_lead(client, model, row)
        row["summary"] = summary
        processed_results.append(row)

    # 5. Save & Report
    if processed_results:
        csv_utils.save_results(output_path, processed_results)
        display_results(processed_results)
        logger.info(f"Successfully saved {len(processed_results)} summaries to {output_path}")
    else:
        logger.warning("No valid leads were found to process.")

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "--file",
            type=str,
            default="leads.csv",
            help="Path to the input CSV file"
        )
        args = parser.parse_args()
        
        dir_name = os.path.dirname(args.file)
        base_name = os.path.basename(args.file)
        output_path = os.path.join(dir_name, f"summarized_{base_name}")
        
        main(args.file, output_path)
    except KeyboardInterrupt:
        print("\n\n[Interrupted] Lead summarization aborted by user.")
    except Exception as e:
        logger.critical(f"A fatal error occurred: {e}")
