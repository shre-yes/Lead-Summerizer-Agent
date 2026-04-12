# Lead Summarizer Agent

A professional Python-based AI agent that transforms raw lead data into concise, actionable summaries using the Groq (Llama-3) LLM.

---

## 📋 Table of Contents
- [About the Project](#-about-the-project)
- [Problem Statement](#-problem-statement)
- [Tech Stack](#-tech-stack)
- [Features](#-features)
- [Demo](#-demo)
- [Project Structure](#-project-structure)
- [Approach & Challenges](#-approach--challenges)
- [Setup](#-setup)
- [Usage](#-usage)
- [Testing](#-testing)
- [Future Improvements](#-future-improvements)
- [License](#-license)


---

## 📖 About the Project
The **Lead Summarizer Agent** is designed to streamline sales workflows by automatically processing bulk lead data from CSV files. It leverages high-performance Large Language Models (LLMs) via the Groq API to distill complex notes and background information into clear, 1-2 sentence insights.

## ❗ Problem Statement
Manual lead qualification is time-consuming and prone to human error. Sales teams often face:
- **Data Overload**: Sifting through hundreds of raw entries to find high-intent prospects.
- **Inconsistent Formatting**: Messy CSV files with unpredictable encodings and delimiters.
- **Resource Drain**: Spending valuable hours on summarization instead of direct outreach.

This agent automates the "first pass" of lead analysis, allowing teams to focus on strategy and closing deals.

## 🛠️ Tech Stack
| Component | Technology |
| :--- | :--- |
| **Language** | Python 3.10+ |
| **AI Model** | Llama-3 (via Groq Cloud) |
| **Data Parsing** | Standard `csv` with `Sniffer` |
| **Env Management** | `python-dotenv` |
| **Logging** | Native `logging` library |

---

## 🚀 Features

### Core Functionality
- **AI-Powered Summarization**: Generates 1-2 line summaries focusing on key intent and contact details.
- **Smart CSV Detection**: Automatically identifies file encodings (UTF-8, CP1252, etc.) and delimiters (commas, semicolons, tabs).
- **Modular Design**: Clean separation of concerns between lead processing, API communication, and file utilities.
- **Performance Reporting**: Displays a clean, formatted summarization report in the terminal after processing.

### Robustness & Safety
- **Pre-flight Checks**: Validates if the output file is writable (e.g., checks if it is open in Excel) before using API credits.
- **Graceful Retries**: Handles common decoding errors by cycling through multiple encoding formats.
- **Failure Isolation**: If one lead fails to summarize, the script logs the error and continues to the next lead rather than crashing.

### Edge Case Handling
- **Binary Data Prevention**: Detects if a user accidentally uploads a binary file (like Excel `.xlsx`) and prevents corruption.
- **Malformed Input**: Skips rows with mismatched column counts or missing data while logging warnings.
- **Header Normalization**: Automatically strips whitespace and converts headers to lowercase for flexible input mapping.

---

## 📺 Demo

### Terminal Report
When processing is complete, the agent generates a formatted report in your console:
```text
====================================================================================================
                                     LEAD SUMMARIZATION REPORT                                      
====================================================================================================

1. John Doe @ TECH SOLUTIONS
   Contact: john.doe@techsolutions.com | +1234567890
   Summary: John Doe is interested in AI integration for customer support and wants to schedule a demo next Tuesday.
--------------------------------------------------
...
====================================================================================================
                                           END OF REPORT                                            
====================================================================================================
```

## 🎬 Demo Video

[Watch Demo](https://github.com/shre-yes/Lead-Summerizer-Agent/releases/download/v.1.0/Assignment.1.mp4)

---

## 📂 Project Structure
```text
Summerizer Agent/
├── .env                # API Keys (Git ignored)
├── .gitignore          # Git configuration
├── csv_utils.py        # CSV parsing & normalization logic
├── leads_sample.csv    # Public sample data
├── llm_client.py       # Groq API integration
├── main.py             # Main entry point & orchestration
├── requirements.txt    # Project dependencies
└── README.md           # Documentation
```

---

## 🧠 Approach & Challenges

### The Strategy
We adopted a **Modular Architecture** to ensure the agent is maintainable and extensible. 
- **The LLM Strategy**: We used a low-temperature (0.3) setting to ensure consistency and minimize "hallucinations" while keeping the summary strictly limited to 1-2 sentences.
- **The Data Strategy**: Since CSVs are notoriously inconsistent, we implemented a "multi-layer detection" system using `csv.Sniffer` for delimiters and a prioritized encoding list for file reading.

### Key Challenges
- **CSV Robustness**: Handling files exported from different systems (Excel, Google Sheets, CRM exports) which often use different delimiters and encodings.
- **Error Propagation**: Preventing a single API timeout or malformed row from failing the entire batch process.
- ****: 

---

## 🛠️ Setup

1. **Setup virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**:
   Create a `.env` file in the root directory and add your Groq API key:
   ```env
   GROQ_API_KEY=your_api_key_here
   MODEL=llama-3.3-70b-versatile
   ```

---

## 📂 Usage

Run the script by providing the path to your input CSV. The file can be within the project folder or anywhere on your system:

**Using the included sample:**
```bash
python main.py --file leads_sample.csv
```

**Using a file in another directory (Relative or Absolute):**
```bash
# Relative path
python main.py --file ../data/my_leads.csv

# Absolute path
python main.py --file "C:/Users/Documents/Marketing/contacts.csv"
```

*The script will automatically generate a results file (prefixed with `summarized_`) in the same folder as your input file.*

---

## 🧪 Testing

To verify the installation and core functionality:

1. **Run with Sample Data**:
   ```bash
   python main.py --file leads_sample.csv
   ```
2. **Check Output**:
   - Verify that `summarized_leads_sample.csv` was created.
   - Check the terminal for the "LEAD SUMMARIZATION REPORT".
3. **Validate Results**:
   Open the generated CSV and ensure the `summary` column contains AI-generated text for each lead.

---

## 🔮 Future Improvements
- [ ] **Asynchronous Processing (Concurrency):** Implement `AsyncGroq` and `asyncio.gather` with a semaphore to speed up API calls.
- [ ] **Batching Logic:** Implement chunked lead processing using JSON mode to reduce total API call count.
- [ ] **Excel Support**: Directly read/write `.xlsx` files without conversion.

---

## 📝 License
Distributed under the MIT License. See `LICENSE` for more information.
