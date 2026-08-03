import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

class ChatApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.layout.add_widget(Label(text="Groq AI Chatbot", font_size='20sp', size_hint_y=None, height=40))
        
        self.api_input = TextInput(hint_text="Enter Groq API Key here...", multiline=False, size_hint_y=None, height=50)
        self.layout.add_widget(self.api_input)
        
        self.chat_history = Label(text="Welcome! Enter API Key and start chatting.", size_hint_y=None, markup=True)
        self.chat_history.bind(texture_size=lambda instance, value: setattr(instance, 'height', value[1]))
        
        self.scroll = ScrollView(size_hint=(1, 1))
        self.scroll.add_widget(self.chat_history)
        self.layout.add_widget(self.scroll)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=5)
        self.msg_input = TextInput(hint_text="Type a message...", multiline=False)
        send_btn = Button(text="Send", size_hint_x=0.3)
        send_btn.bind(on_press=self.send_message)
        
        input_layout.add_widget(self.msg_input)
        input_layout.add_widget(send_btn)
        self.layout.add_widget(input_layout)
        
        return self.layout

    def send_message(self, instance):
        user_text = self.msg_input.text.strip()
        api_key = self.api_input.text.strip()
        
        if not user_text:
            return
        if not api_key:
            self.chat_history.text += "\n[color=ff0000]System: Please enter a valid API Key![/color]"
            return
            
        self.chat_history.text += f"\n\n[b]You:[/b] {user_text}"
        self.msg_input.text = ""
        
        Clock.schedule_once(lambda dt: self.get_ai_response(user_text, api_key), 0.1)

    def get_ai_response(self, user_text, api_key):
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": [{"role": "user", "content": user_text}]
        }
        
        try:
            res = requests.post(url, json=payload, headers=headers, timeout=10)
            if res.status_code == 200:
                response_data = res.json()
                bot_reply = response_data['choices'][0]['message']['content']
                self.chat_history.text += f"\n\n[b]AI:[/b] {bot_reply}"
            else:
                self.chat_history.text += f"\n\n[color=ff0000]API Error {res.status_code}:[/color] {res.text}"
        except Exception as e:
            self.chat_history.text += f"\n\n[color=ff0000]Error:[/color] {str(e)}"

if __name__ == '__main__':
    ChatApp().run()
        
