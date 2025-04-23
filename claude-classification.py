import anthropic
import pandas as pd
import time
from pathlib import Path
import os

def parse_response(response_text):
    """
    Parse Claude's response text to extract classification results.
    Returns a list of dictionaries with classification results.
    """
    results = []
    
    # Split response by lines and filter out non-data lines
    lines = response_text.strip().split('\n')
    data_lines = [line.strip() for line in lines if ',' in line]  # Using comma as separator based on your requested format
    
    for line in data_lines:
        # Split by the separator
        try:
            item_id, result = line.split(',', 1)
            
            # Create result record
            result = {
                'ID': item_id.strip(),
                'Quality': result.strip().replace('"', '')  # Remove any quotes
            }
            results.append(result)
        except Exception as e:
            print(f"Error parsing line: {line}, Error: {e}")
    
    return results

# File paths
CSV_DIR = Path("csv-files")
PROMPT_FILE = Path("classification_prompt_effectiveness.md")
PLATFORM = "webmd-effectiveness-test"  # Change to "amazon" or "reddit" as needed

# Load your data
df = pd.read_csv(CSV_DIR / f"{PLATFORM}.csv")

# Load your prompt from file
with open(PROMPT_FILE, "r") as f:
    classification_prompt = f.read()

# Setup API client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

results = []
batch_size = 100

# Process in batches
for i in range(0, len(df), batch_size):
    batch = df.iloc[i:i+batch_size]
    
    # Format the batch data
    batch_text = "\n".join([f"{row['ID']},{row['Product']},{row['Website']},\"{row['Review']}\"" for _, row in batch.iterrows()])
    
    # Create the prompt with your classification instructions
    prompt = f"""{classification_prompt}
    
    Here are the reviews to classify:
    {batch_text}
    """
    
    try:
        # Call Claude API
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        
        # Parse response and extract classifications
        classifications = parse_response(response.content[0].text)
        results.extend(classifications)
        
        print(f"Processed batch {i//batch_size + 1}/{(len(df) + batch_size - 1)//batch_size} ({len(classifications)} items)")
        
        # Sleep to avoid rate limits
        time.sleep(1)
        
    except Exception as e:
        print(f"Error processing batch {i}-{i+batch_size}: {e}")
        # Could add retry logic here

# Save all results
results_df = pd.DataFrame(results)
results_df.to_csv(CSV_DIR / f"classified_results_{PLATFORM}.csv", index=False)
print(f"Processing complete. {len(results)} records classified.")