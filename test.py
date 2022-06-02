from guizero import App, Text, TextBox, PushButton

app = App(title = "Magic price finder")
my_text = TextBox(app, text = "Magic", width="fill")
my_button = PushButton(app, text = "Find price", command = lambda: print(my_text.value))

print(my_text.value)
app.display()