from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import os


class MichaelJacksonChatbot:
    def __init__(self, model_path):
        """
        Initializes the chatbot with the trained model.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"Using device: {self.device}")

        print("Loading model and tokenizer...")
        self.tokenizer = GPT2Tokenizer.from_pretrained(model_path)
        self.model = GPT2LMHeadModel.from_pretrained(model_path)

        special_tokens = {
            "bos_token": "<|startoftext|>",
            "eos_token": "<|endoftext|>",
            "pad_token": "<|pad|>",
            "additional_special_tokens": ["<|michael|>"],
        }
        self.tokenizer.add_special_tokens(special_tokens)
        self.model.resize_token_embeddings(len(self.tokenizer))

        self.model.to(self.device)
        self.model.eval()
        print("Model loaded successfully!")

    def generate_response(self, user_prompt, max_new_tokens=100, temperature=0.7):
        """
        Generates a response for the given prompt with better completion control.

        Args:
            user_prompt (str): The initial text from the user.
            max_new_tokens (int): Maximum number of new tokens to generate.
            temperature (float): Controls randomness (0.0 = deterministic, 1.0 = more random).
        """
        input_text = f"<|startoftext|><|michael|>{user_prompt}"
        encoded_inputs = self.tokenizer.encode(input_text, return_tensors="pt").to(
            self.device
        )

        # Tokens that indicate the end of a sentence
        end_tokens = [".", "!", "?", "\n"]
        end_token_ids = [self.tokenizer.encode(token)[-1] for token in end_tokens]

        generated_outputs = self.model.generate(
            encoded_inputs,
            max_new_tokens=max_new_tokens,
            min_new_tokens=20,  # Ensures a minimum response length
            num_return_sequences=1,
            no_repeat_ngram_size=3,  # Avoids 3-gram repetitions
            repetition_penalty=1.2,
            temperature=temperature,
            top_p=0.92,
            top_k=50,  # Limits options to the 50 most probable
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            # Forces termination at an end token
            forced_eos_token_id=end_token_ids[0],
            # Increases the probability of end tokens
            typical_p=0.95,
        )

        decoded_response = self.tokenizer.decode(
            generated_outputs[0], skip_special_tokens=True
        )

        # Ensure the response ends at a natural stopping point
        if not any(decoded_response.endswith(token) for token in end_tokens):
            last_sentence_end_index = max(
                decoded_response.rfind("."),
                decoded_response.rfind("!"),
                decoded_response.rfind("?"),
            )
            if last_sentence_end_index != -1:
                decoded_response = decoded_response[: last_sentence_end_index + 1]
            else:
                decoded_response = decoded_response + "..."

        return decoded_response

    def adjust_response_length(self, response_text):
        """
        Adjusts the response length to end at a natural stopping point.
        """
        # Find the last natural end point
        end_markers = [". ", "! ", "? "]
        last_end_position = -1

        for marker in end_markers:
            pos = response_text.rfind(marker)
            last_end_position = max(last_end_position, pos)

        if last_end_position != -1:
            return response_text[: last_end_position + 1].strip()
        return response_text.strip()
