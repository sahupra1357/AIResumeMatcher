import os
from typing import List
from dotenv import load_dotenv
# Load environment variables
load_dotenv()

def generate_llm_response(system_prompt, user_prompt, llm_type="openai", temperature=0.7, max_tokens=500): 

    import inspect
    caller_frame = inspect.currentframe().f_back
    caller_name = caller_frame.f_code.co_name
    print(f"Called by method: {caller_name}")

    if llm_type == "openai":
        try:
            print("Using OpenAI LLM")
            from openai import OpenAI

            model = os.getenv("OPENAI_MODEL")
            client = OpenAI()

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = client.responses.create(
                model=model,
                input=messages,
            )
            ## Print response number of token used and execution time
            try:
                usage = response.usage
                # Check available attributes
                if hasattr(usage, 'input_tokens'):
                    print(f"Tokens used: input={usage.input_tokens}, output={usage.output_tokens}, total={usage.total_tokens}")
                elif hasattr(usage, 'prompt_tokens'):
                    print(f"Tokens used: prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")
                else:
                    print(f"Usage info: {usage}")
                
                if hasattr(usage, 'total_cost'):
                    print(f"Cost: ${usage.total_cost:.6f}")

                if hasattr(response, 'created_at'):
                    created_time = response.created_at
                if hasattr(response, 'completed_at'):
                    completed_time = response.completed_at
                total_time = (completed_time - created_time) if (hasattr(response, 'created_at') and hasattr(response, 'completed_at')) else 0
                print(f"Total execution time: {total_time} seconds")

            except Exception as e:
                print(f"Could not retrieve usage stats: {e}")

            
            # print("Response: ", response.output_text)
            print("---------------------------------")
            print()
            return response.output_text
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Error generating LLM response."    
    elif llm_type == "openai_reasoning":
        try:
            print("Using OpenAI Reasoning LLM")
            from openai import OpenAI

            model = os.getenv("OPENAI_REASONING_MODEL")
            client = OpenAI()

            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]

            response = client.responses.create(
                model=model,
                input=messages,
            )

            ## Print response number of token used and execution time
            try:
                usage = response.usage
                # Check available attributes
                if hasattr(usage, 'input_tokens'):
                    print(f"Tokens used: input={usage.input_tokens}, output={usage.output_tokens}, total={usage.total_tokens}")
                elif hasattr(usage, 'prompt_tokens'):
                    print(f"Tokens used: prompt={usage.prompt_tokens}, completion={usage.completion_tokens}, total={usage.total_tokens}")
                else:
                    print(f"Usage info: {usage}")
                
                if hasattr(usage, 'total_cost'):
                    print(f"Cost: ${usage.total_cost:.6f}")

                if hasattr(response, 'created_at'):
                    created_time = response.created_at
                if hasattr(response, 'completed_at'):
                    completed_time = response.completed_at
                total_time = (completed_time - created_time) if (hasattr(response, 'created_at') and hasattr(response, 'completed_at')) else 0
                print(f"Total execution time: {total_time} seconds")

            except Exception as e:
                print(f"Could not retrieve usage stats: {e}")

            print("Response: ", response.output_text)
            print("---------------------------------")
            print()
            return response.output_text
        except Exception as e:
            print(f"Error generating LLM response: {e}")
            return "Error generating LLM response."    
    elif llm_type == "claude":
        print("Using Claude LLM")
        from anthropic import Anthropic
        model=os.getenv("CLAUDE_MODEL")
        api_key=os.getenv("ANTHROPIC_API_KEY")
        client = Anthropic(api_key=api_key)
        response = client.messages.create(
            model=model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.content[0].text.strip()
    elif llm_type == "google":
        print("Using Google LLM")
        from google import genai
        model=os.getenv("GOOGLE_MODEL")
        api_key=os.getenv("GOOGLE_API_KEY")

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        return response.choices[0].message.content
    elif llm_type == "deepseek":
        print("Using Deepseek LLM")
        from google import genai
        model=os.getenv("DEEPSEEK_MODEL")
        api_key=os.getenv("DEEPSEEK_API_KEY")

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.deepseek.com"
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        print("Response: ", response.choices[0].message.content)
        print("---------------------------------")
        print()
        return response.choices[0].message.content
    elif llm_type == "groq":
        print("Using groq LLM")
        from google import genai
        model=os.getenv("GROQ_MODEL")
        api_key=os.getenv("GROQ_API_KEY")

        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
        )

        return response.choices[0].message.content
    

##### Auudio to text and text to 

import whisper

def load_STT_model(llm_type="whisper"):
    import ssl
    import certifi
    ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())
    # os.environ["PYTHONHTTPSVERIFY"] = "0"
    if llm_type == "whisper":
        """Load and return the Whisper model."""
        try:
            model = whisper.load_model(
                "base",  # model size: tiny, base, small, medium, large
                device="cpu",  # or "cuda" if you have a GPU available
                download_root="./models",  # specify the directory to store models
                in_memory=True  # set to True to load model into memory (default is False)
                )
            return model
        except Exception as e:
            print(f"Error loading model: {e}")
            return None


def transcribe_audio(audio_file_path, llm_type="whisper"):
    if llm_type == "whisper":
        model = load_STT_model(llm_type)
        if model is None:
            return None

        try:
            if audio_file_path:
                result = model.transcribe(audio_file_path, fp16=False)
                return result["text"]
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
    elif llm_type == "openai":
        from openai import OpenAI
        model=os.getenv("OPENAI_AUDIO_MODEL")
        client = OpenAI()
        audio_file = open(audio_file_path, "rb")

        result = client.audio.transcriptions.create(
            model=model,
            file=audio_file,
            response_format="text"
        )

        return result
    elif llm_type == "google_openai":
        from google import genai
        model=os.getenv("GOOGLE_MODEL")
        api_key=os.getenv("GOOGLE_API_KEY")

        import base64
        from openai import OpenAI

        client = OpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )

        if audio_file_path.endswith(".mp3"):
            audio_format = "mp3"
        elif audio_file_path.endswith(".wav"):
            audio_format = "wav"
        else:
            print("Unsupported audio format. Please use .mp3 or .wav files.")
            return None
        
        with open(audio_file_path, "rb") as audio_file:
            base64_audio = base64.b64encode(audio_file.read()).decode('utf-8')

        response = client.chat.completions.create(
            model="gemini-2.0-flash",
            messages=[
            {
                "role": "user",
                "content": [
                    {
                    "type": "text",
                    "text": "Transcribe this audio",
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": base64_audio,
                            "format": audio_format
                        }
                    }
                ],
            }
        ],
        )

        return response.choices[0].message.content
    elif llm_type == "google":
        from google import genai
        model=os.getenv("GOOGLE_MODEL")
        api_key=os.getenv("GOOGLE_API_KEY")

        from google import genai

        client = genai.Client()
        myfile = client.files.upload(file=audio_file_path)
        prompt = 'Generate a transcript of the speech.'

        response = client.models.generate_content(
            model=model,
            contents=[prompt, myfile]
        )

        return response.text
    else:
        print(f"LLM type {llm_type} not supported for transcription.")
        return None

def generate_embedding(text: str, llm_type="openai") -> List[float]:
    """
    Generate embedding vector for the given text using specified LLM.
    """
    if llm_type == "openai":
        from openai import OpenAI
        model=os.getenv("OPENAI_EMBEDDING_MODEL")
        client = OpenAI()

        response = client.embeddings.create(
            model=model,
            input=text
        )

        return response.data[0].embedding
    else:
        print(f"LLM type {llm_type} not supported for embeddings.")
        return []