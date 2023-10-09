import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.graphics import Canvas, Color, Rectangle


from langchain.base_language import BaseLanguageModel
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate

#openai_api_key = os.environ.get('OPENAI_API_KEY')
openai_api_key = "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"
llm_model = "gpt-3.5-turbo-0301"
llm = ChatOpenAI(model=llm_model, temperature=0.0, openai_api_key=openai_api_key)
dictionary_template = """You are an english teacher. \
    You will give the meaning elaborately, explain the nuances if\
    there is any, give two example sentences,\
    synonyms and antonyms of the word or phrase or idiom: {word}. The example sentences should be long enough for the meaning to be apparent.\
    If the word is not an english word or phrase\
    say that <<<It is not an English Word.>>> Also mention the parts of speech. If there is spelling mistakes\
    guess the nearest meaningful word, saying <<<Did you mean <your guess>?>>> in the begining. Use the following layout\
    
    word (part of speech): meaning goes here

    Example Sentences: 

    synonyms:
    antonyms:

    Write the word in lower case letters.
    If the word can be used as different parts of speech, for every part of speech, you give the meaning, example sentences,\
    synonyms and antonyms. Use the same layout.

    Please do not use any unnecessary delimitation in your response.

    """
prompt_template = ChatPromptTemplate.from_template(dictionary_template)

class MainApp(App):

    title = 'English-to-English Dictionary'

    def build(self):
        Window.clearcolor = (0.93, 0.75, 0.75, 1) # Light Scarlet 

        layout = BoxLayout(orientation='vertical', padding=[20, 20, 20, 20], spacing=10)

        # Input section
        h_layout = BoxLayout(spacing=10, size_hint_y=None, height=44)

        self.user_input = TextInput(hint_text="Enter word or phrase", multiline=False, size_hint_x=0.8, background_color=(1, 1, 1, 1), border=(5, 5, 5, 5))
        self.user_input.bind(on_text_validate=self.on_enter)

        self.response_btn = Button(text="Get Response", size_hint_x=0.2, background_color=(0.46, 0.16, 0.75, 1), color=(1, 1, 1, 1), background_normal='', background_down='')
        self.response_btn.bind(on_press=self.button_down, on_release=self.button_up)

        h_layout.add_widget(self.user_input)
        h_layout.add_widget(self.response_btn)

        layout.add_widget(h_layout)

        # Rectangular area with orange background below the input box
        scroll_container = BoxLayout(padding=[10, 10, 10, 10])  # Adjust padding for inner margin
        with scroll_container.canvas.before:
            Color(0.19, 0.40, 0.60, 1)  # Blue color
            self.rect = Rectangle(pos=scroll_container.pos, size=scroll_container.size)

        # Update the rect when size and pos of container change
        scroll_container.bind(size=self._update_rect, pos=self._update_rect)

        # Output section
        self.response_label = Label(text="", halign="left", valign="top", size_hint_y=None, text_size=(Window.width - 60, None))
        self.response_label.bind(texture_size=self.response_label.setter('size'))

        scroll_view = ScrollView(do_scroll_x=False, size_hint=(1, 1))
        scroll_view.add_widget(self.response_label)

        scroll_container.add_widget(scroll_view)
        layout.add_widget(scroll_container)

        return layout
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    

    def button_down(self, instance):
        """Handle button press event."""
        instance.background_color = (0.34, 0.24, 0.45, 1)  # Change to a darker shade

    def button_up(self, instance):
        """Handle button release event."""
        # Clear the previous response
        self.response_label.text = ""

        # Reset the button color to the original color
        instance.background_color = (0.46, 0.16, 0.75, 1) 
        
        # Schedule the get_response call after a 0.1 second delay
        Clock.schedule_once(self.get_response, 0.1)  
   

    def get_response(self, dt):  # Add 'dt' to accept the delta-time argument from the Clock
        self.response_label.text = ""
        
        word_or_phrase = self.user_input.text
        if word_or_phrase:
            word_prompt = prompt_template.format_messages(word=word_or_phrase)
            gpt_response = llm(word_prompt)
            
            # Update the label with the response from GPT
            self.response_label.text = gpt_response.content
        else:
            self.response_label.text = "Please enter a word or phrase."


    def on_enter(self, instance):
        # Clear the previous response
        self.response_label.text = ""
        
        # Continue with fetching the new response
        Clock.schedule_once(self.get_response, 0.1)  # Add a small delay before showing "Loading..."



if __name__ == '__main__':
    MainApp().run()
