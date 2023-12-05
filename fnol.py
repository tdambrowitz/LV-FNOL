import openai
from docx import Document
import os
import soundfile as sf
import numpy as np
import streamlit as st
import time
from pydub import AudioSegment
from moviepy.editor import *
import math
from openai import OpenAI
import csv
import ast



openai.api_key = st.secrets["OPENAI_API_KEY"]

client = OpenAI()

# Streamlit Configuration
st.set_page_config(
    page_title="Lightyear PO's",
    page_icon=":microphone:"
)

def get_state_variable(var_name, default_value):
    if 'st_state' not in st.session_state:
        st.session_state['st_state'] = {}
    if var_name not in st.session_state['st_state']:
        st.session_state['st_state'][var_name] = default_value
    return st.session_state['st_state'][var_name]

# Initialize session state for authentication
if 'is_authenticated' not in st.session_state:
    st.session_state.is_authenticated = False

    
suppliers = [
    "ADT Fire and Security Plc",
    "Advanced Radiators",
    "Ancaster Group Ltd",
    "Barons Automotive Ltd",
    "Basingstoke MOT & Tyre Centre",
    "Bassetts Citroen",
    "Bassetts Honda",
    "Baylis Vauxhall",
    "Blade - Heritage Honda",
    "Bradleys Honda",
    "Breeze Volkswagen",
    "Brighton Mitsubishi",
    "Bristol Honda",
    "Bristol Street Motors",
    "Bristol Street Motors Gloucester",
    "Brown Brothers Ltd - (PPG)",
    "Caffyns Plc",
    "Cambridge Accident Repair Centre",
    "Cambridge Garage Ltd",
    "Cars2 - Mazda & Hyundai",
    "Cars2 - MG",
    "Charles Trent Ltd",
    "Cheltenham Borough Council",
    "Circle Leasing Limited",
    "Colne Tyre Centre",
    "Copper Jax Contract Maintenance",
    "Cotswold Motor Group Plc",
    "Dave Daley",
    "Days Motor Group",
    "Diagnostec",
    "Dick Lovett BMW Bristol",
    "Dick Lovett BMW Swindon",
    "Dick Lovett BMW Westbury",
    "Dick Lovett Jaguar/Landrover",
    "Dorset Autospares",
    "Doves Vauhall",
    "Drayton Group (Merc Benz of Stoke)",
    "Drive",
    "Dunns Automotive Ltd",
    "Eastbourne Car Keys - Nicholas Prout",
    "Eastbourne Tyre Co",
    "Eden Basingstoke",
    "Endeavour Volvo",
    "Euro Car Parts",
    "Evans Halshaw - Vauxhall",
    "Express Motor Workshop",
    "FG Barnes",
    "Fish Brothers Toyota",
    "Fordthorne Volvo",
    "General Vehicle Services",
    "Glyn Hopkin",
    "Gray Scott Electrical Contractors Ltd",
    "Grenson Motor Co Ltd (Acorn Group)",
    "Group 1 - BMW",
    "Group 1 - JLR",
    "Group 1 - Mercedes",
    "GSF Car Parts Limited",
    "Harrats",
    "Harwoods Chichester",
    "Harwoods Pulborough",
    "Havant Motor Factors",
    "Hendy Group Ltd",
    "Highways",
    "Hills Salvage",
    "Hl Motors Ltd",
    "Holdcroft Honda Ltd",
    "Holdcroft Hyundai Ltd",
    "Holdcroft MG Stoke Ltd",
    "Holdcroft Nissan Ltd",
    "Holdcroft Renault Ltd",
    "Honda Crown",
    "Horizon Motor Company",
    "HSF Group - Volvo",
    "Hummingbird Motors",
    "Inchcape Land Rover",
    "Inchcape Toyota Guildford",
    "Islington Motor Group",
    "Jemca Lexus/Toyota Reading",
    "J & J Motors",
    "J&J Motors",
    "Johnsons Ltd - Mazda",
    "Johnsons Ltd - Toyota",
    "Johnsons Ltd - Volvo",
    "John Wilkins Cars",
    "Ken Jervis",
    "Kwik-Fit",
    "Lansdown Mazda",
    "Lightyear Test PO's",
    "Listers Group",
    "LKQ Coatings",
    "Lookers Motor Group Ltd",
    "Magna Mazda",
    "Magna Motor Mistusubishi/Subaru",
    "Managed Ink",
    "Marshall Land Rover Newbury",
    "Marshalls BMW Salisbury",
    "Marshalls BMW Salisbury",
    "Marshalls Lexus",
    "Marshalls Mercedes Southampton",
    "Martins Vw / Nissan / Volvo",
    "Mercedes-Benz Bolton (Marshalls)",
    "Mercedes Benz of Bristol (Sytner)",
    "Mercedes-Benz of Southampton",
    "Mercedes Benz Salisbury",
    "Midhurst Engineering & Motor Co. Ltd",
    "Minden Systems Ltd",
    "Minster Cleaning",
    "M & M Cleaning Services",
    "Motorline",
    "Motor Parts Direct Ltd",
    "Motorscreen Ltd",
    "MRG Volvo - Chippenham Motor Co",
    "Office Watercoolers Ltd",
    "One Offs",
    "Pace Parts",
    "Partridge BMW",
    "Partsplus",
    "Pentagon Lincoln",
    "Penton Motor Group",
    "Pinkstones",
    "Platinum Hyundai",
    "Platinum Hyundai",
    "Platinum Nissan",
    "Platinum Renault/Dacia",
    "Platinum Toyota - Bath",
    "Platinum Toyota - Trowbridge",
    "Platinum Vauxhall - Trowbridge",
    "Porsche Centre Portsmouth",
    "PPG Industries (UK) Ltd - Pine Tree Consulting - Actiweb Fee",
    "Prasco UK Ltd",
    "Primrose Radar Calibration",
    "Proven Motor Co Ltd",
    "Recovery World Ltd",
    "Renault Retail Group",
    "Richmond Cars Ltd Bognor",
    "Richmond Cars Ltd Fareham",
    "Richmond Cars Ltd Portsmouth",
    "Riverside Motors",
    "Roadworthy Bristol",
    "Rybrook JGL Stoke",
    "Rybrook JGL Warrington",
    "Rye Motors Limited",
    "Rygor Mercedes-Benz",
    "Sage UK",
    "Sandal BMW Wakefield",
    "Sandown Mercedes Salisbury",
    "Screen Genies",
    "SES Autoparts Ltd",
    "SG Petch",
    "Silverlake Automotive Recycling",
    "Simpsons",
    "Slated Barn Garage",
    "Snows BMW / Mini",
    "Snows Fiat / Alpha Romeo / Jeep",
    "Snows Peugeot / Mazda",
    "Snows Seat / Suzuki",
    "Snows Toyota / Lexus",
    "Snows Volvo / Kia",
    "Soper BMW Lincoln",
    "Spanesi Automotive Equipment Ltd",
    "Stars Garage",
    "Stellantis & You",
    "Steven Eagell Toyota",
    "Stoneacre Volvo Lincoln",
    "Stonearce Fiat Lincoln",
    "Stratstone Land Rover Cardiff",
    "Synetiq Ltd",
    "Sytner JLR Bristol",
    "Sytner Mercedes",
    "Test Supplier",
    "TG Holdcroft - Mazda",
    "Tomo Motor Parts Ltd",
    "Tony Levoi",
    "Tood Engineering",
    "Trade Part Specialists Ltd",
    "TW White & Sons",
    "Uniplate Limited",
    "Vantage Group Toyota",
    "Vertu Honda - Lincoln",
    "Vertu JLR - Bolton",
    "Vertu JLR - Leeds",
    "Vine ( Fisher German )",
    "Vines BMW Guildford",
    "Volvo Cars Poole",
    "Warners Motor Group",
    "Wessex Garages",
    "West Riding Hyundai",
    "Wheel Traders ltd",
    "Williams BMW Manchester",
    "WR Davies Motor Group",
    "Yeomans Ltd Honda",
    "Yeomans Ltd Nissan",
    "Yeomans Ltd Toyota"
]


def display_page():

    # Function to split audio
    def split_audio_sf(audio_path, target_chunk_size, max_file_size=25 * 1024 * 1024):
        # Read the audio data
        data, samplerate = sf.read(audio_path)
        total_samples = len(data)

        while True:
            chunk_samples = int(target_chunk_size * samplerate)

            # Check if the chunk size produces files larger than max_file_size
            num_chunks = math.ceil(total_samples / chunk_samples)
            print(f"Splitting audio into {num_chunks} chunks of {chunk_samples} samples each")
            estimated_size_per_chunk = os.path.getsize(audio_path) / num_chunks
            print(f"Estimated size per chunk: {estimated_size_per_chunk} bytes")

            if estimated_size_per_chunk > max_file_size:
                # If chunks are too large, reduce the target chunk size and recalculate
                target_chunk_size -= 10  # Reduce by 10 seconds and retry
                if target_chunk_size <= 0:
                    raise ValueError("Cannot split audio into chunks smaller than the max file size.")
                continue  # If still too large, loop back and try with reduced chunk size

            # If the estimated size per chunk is within the limit, proceed to create chunks
            chunks = [(data[start:start + chunk_samples], samplerate) for start in range(0, total_samples, chunk_samples)]
            break  # If chunk sizes are okay, break out of the loop and return chunks

        return chunks

    def transcribe_chunks_sf(chunks):
        transcriptions = []
        
        for i, (data, samplerate) in enumerate(chunks):
            temp_path = f'temp_chunk_{i}.wav'
            sf.write(temp_path, data, samplerate)

            # Check file size
            file_size = os.path.getsize(temp_path)
            if file_size > 26214400:  # 25 MB in bytes
                print(f"Skipping chunk {i} due to large size: {file_size} bytes")
                os.remove(temp_path)
                continue

            transcription = transcribe_audio(temp_path)
            transcriptions.append(transcription)
            os.remove(temp_path)
            
        return ' '.join(transcriptions)


    def transcribe_audio(audio_file_path):
        with open(audio_file_path, 'rb') as audio_file:
            transcription = openai.audio.transcriptions.create(
                model="whisper-1", 
                file=audio_file,
                language="en"  # Set the language to English
            )
        return transcription.text  # Here, we use .text instead of ['text']



    def meeting_minutes(transcription):
        word_count = len(transcription.split())
        # Calculate sleep duration: 4 seconds for every 1000 words
        sleep_duration = (word_count / 1000) * 1

        # Ensure minimum sleep time (e.g., 2 seconds) if transcription is very short
        sleep_duration = max(sleep_duration, 2)

        # Sleep dynamically based on the number of words in the transcription
        time.sleep(sleep_duration)

        abstract_summary = parse_text(transcription)
        time.sleep(sleep_duration)  # Repeat sleep after each processing step

        return {
            'abstract_summary': abstract_summary,
        }
        
    def parse_text(transcription):
        prompt = (
            "Analyze the following transcription and output the extracted information as a structured dictionary with keys and values. "
            "The keys are 'PO Number', 'Supplier Name', 'PO Date', 'PO Reference', 'PO Line Description', 'PO Line Qty', 'Unit Price', and 'Location'. "
            "Each key should correspond to a value extracted from the transcription. PO Line Quantity will always be 1. If multiple parts are ordered format the value as a text string listing them.\n\n"
            f"All Valid Suppliers:\n\"{suppliers}\"\n\n"
            "You must use a supplier from this list, please select the closest match to the one in the transcription.\n\n"
            f"Please format the extracted information in a clear and structured manner as shown in the examples below.\n"
            "Example 1:\n"
            "{\n"
            "    'PO Number': 'F23110071',\n"
            "    'Supplier Name': 'Euro Car Parts',\n"
            "    'PO Date': '28/11/2023',\n"
            "    'PO Reference': 'MJ64LWU',\n"
            "    'PO Line Description': 'Front Bumper and LH Headlamp',\n"
            "    'PO Line Qty': '1',\n"
            "    'Unit Price': '247.24',\n"
            "    'Location': 'Crewe'\n"
            "}\n\n"
            "Example 2:\n"
            "{\n"
            "    'PO Number': 'A23110174',\n"
            "    'Supplier Name': 'Brown Brothers',\n"
            "    'PO Date': '28/11/2023',\n"
            "    'PO Reference': 'HG21CZU',\n"
            "    'PO Line Description': 'L/R Wheel and Arch Moulding',\n"
            "    'PO Line Qty': '1',\n"
            "    'Unit Price': '381.56',\n"
            "    'Location': 'Amesbury'\n"
            "}\n\n"
            "Example 3:\n"
            "{\n"
            "    'PO Number': 'L23110065',\n"
            "    'Supplier Name': 'Parts Plus',\n"
            "    'PO Date': '28/11/2023',\n"
            "    'PO Reference': 'T22EMY',\n"
            "    'PO Line Description': 'Front Radar and Radiator',\n"
            "    'PO Line Qty': '1',\n"
            "    'Unit Price': '793.03',\n"
            "    'Location': 'Cheltenham'\n"
            "}\n\n"
            "Now, based on the transcription provided, format the extracted information in a similar structured dictionary:\n\n"
            f"Transcription:\n\"{transcription}\""
            "Provide ONLY the extracted information as a structured dictionary with keys and values. Do not include any other text or information."
        )
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            temperature=0,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=2000,
        )
        # Access the content directly from the response object's attributes
        summary_content = response.choices[0].message.content
        return summary_content
    
    def save_as_csv(abstract_summary, filename):
    # Open the file in write mode
        with open(filename, mode='w', newline='', encoding='utf-8') as file:
            # Create a CSV writer object
            writer = csv.writer(file)

            # Write the headers (dictionary keys)
            headers = abstract_summary.keys()
            writer.writerow(headers)

            # Write the row of data (dictionary values)
            row = abstract_summary.values()
            writer.writerow(row)

    # Parameters
    chunk_length = 2 * 60  # 3 minutes in seconds

    def main():
        # Initialize Streamlit interface
        st.title('Call Transcription and Generation')

        # File uploader allows user to add their own audio
        uploaded_audio = st.file_uploader("Upload audio", type=["wav", "mp3", "m4a"])

        if uploaded_audio is not None:
            # Button to trigger transcription and processing
            if st.button('Transcribe and Analyze'):
                # Process the audio
                with st.spinner('Processing audio...'):
                    audio_path = save_uploaded_file(uploaded_audio)

                    # Split audio
                    with st.spinner('Splitting audio into chunks...'):
                        audio_chunks = split_audio_sf(audio_path, chunk_length)

                    # Transcribe each chunk and concatenate
                    with st.spinner('Transcribing audio... this might take a while'):
                        full_transcription = transcribe_chunks_sf(audio_chunks)

                    # Delete temp file
                    if os.path.exists(audio_path):
                        os.remove(audio_path)

                    # Display transcription
                    st.subheader("Transcription")
                    st.text_area("Full Transcription", full_transcription, height=300)

                    # Generate meeting minutes
                    with st.spinner('Generating formatted data... this might take a while'):
                        minutes = meeting_minutes(full_transcription)

                        # Display meeting minutes details
                        st.subheader("Meeting Minutes")
                        for key, value in minutes.items():
                            st.markdown(f"#### {key.replace('_', ' ').title()}")
                            st.write(value)
                            abstract_summary=value
                            abstract_summary_dict = ast.literal_eval(abstract_summary)
                            st.write(abstract_summary_dict)

                        # Define the CSV file path
                        csv_file_path = 'meeting_minutes.csv'

                        # Save the data as a CSV file
                        save_as_csv(abstract_summary_dict, csv_file_path)

                        # Provide download link for the CSV file
                        with open(csv_file_path, "rb") as file:
                            btn = st.download_button(
                                label="Download formatted data as CSV",
                                data=file,
                                file_name=csv_file_path,
                                mime="text/csv"
                            )

    def convert_to_mp3(audio_path, target_path, bitrate="128k"):
        try:
            audio_clip = AudioFileClip(audio_path)
            audio_clip.write_audiofile(target_path, bitrate=bitrate)
            audio_clip.close()  # It's good practice to close the clip when done
            return True
        except Exception as e:
            print(f"Failed to convert {audio_path} to MP3: {e}")
            return False

    def save_uploaded_file(uploaded_file):
        try:
            file_extension = os.path.splitext(uploaded_file.name.lower())[1]
            base_name = os.path.splitext(uploaded_file.name)[0]
            save_folder = 'temp_files'

            if not os.path.isdir(save_folder):
                os.mkdir(save_folder)

            temp_path = os.path.join(save_folder, uploaded_file.name)
            target_path = os.path.join(save_folder, f"{base_name}.mp3")

            with open(temp_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
                print(f"File saved temporarily at {temp_path}")

            # If the uploaded file is .m4a, convert it to .mp3
            if file_extension == '.m4a':
                print(f"Converting {temp_path} to {target_path}")
                # Verify tempfile exists before attempting conversion
                if os.path.exists(temp_path):
                    convert_to_mp3(temp_path, target_path)
                    # Verify conversion was successful
                    if os.path.exists(target_path):
                        print(f"Conversion successful, file saved at {target_path}")
                        os.remove(temp_path)  # Remove the .m4a file after conversion
                        return target_path
                    else:
                        print(f"Conversion failed, file at {target_path} not found")
                        return None
                else:
                    print(f"Temp file at {temp_path} does not exist, cannot convert")
                    return None
            elif file_extension in ['.mp3', '.wav']:
                return temp_path

        except Exception as e:
            st.error(f"Error handling file: {e}")
            return None

    # start the Streamlit app
    if __name__ == "__main__":
        main()







# Logic for password checking
def check_password():
    if not st.session_state.is_authenticated:
        password = st.text_input("Enter Password:", type="password")


            
        
        if password == st.secrets["db_password"]:
            st.session_state.is_authenticated = True
            st.rerun()
        elif password:
            st.write("Please enter the correct password to proceed.")
            
        blank, col_img, col_title = st.columns([2, 1, 3])

        # Upload the image to the left-most column
        with col_img:
            st.image("https://s3-eu-west-1.amazonaws.com/tpd/logos/5a95521f54e2c70001f926b8/0x0.png")


        # Determine the page selection using the selectbox in the right column
        with col_title:
            #st.title("Created By Halo")
            st.write("")
            st.markdown('<div style="text-align: left; font-size: 40px; font-weight: normal;">Created By Halo*</div>', unsafe_allow_html=True)
            
        blank2, col_img2, col_title2 = st.columns([2, 1, 3])

        # Upload the image to the left-most column
        with col_img2:
            st.image("https://www.notion.so/image/https%3A%2F%2Fs3-us-west-2.amazonaws.com%2Fsecure.notion-static.com%2Fe8f541d9-f3ab-433d-af42-6416222f11f7%2Flv3drgb.jpg?table=block&id=68c88f77-cad9-4e83-bad9-d2e630017be5&spaceId=99a703b7-a660-4095-b6d3-dd73cbc5a1ec&width=380&userId=d6a4f9af-79e1-4d26-8af5-cced5dc1eaa4&cache=v2")


        # Determine the page selection using the selectbox in the right column
        with col_title2:
            
            #st.title("Powered By IRS")
            st.markdown('<div style="text-align: left; font-size: 30px; font-weight: normal;">Powered By LV</div>', unsafe_allow_html=True)
        # Fill up space to push the text to the bottom
        for _ in range(20):  # Adjust the range as needed
            st.write("")

        # Write your text at the bottom left corner
        st.markdown('<div style="text-align: right; font-size: 10px; font-weight: normal;">* Trenton Dambrowitz, Special Projects Manager, is "Halo" in this case.</div>', unsafe_allow_html=True)



    else:
        print("Access granted, welcome to the app.")
        display_page()


check_password()