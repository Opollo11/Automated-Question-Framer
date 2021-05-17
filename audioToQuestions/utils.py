import speech_recognition as sr
from .questiongenerator import QuestionGenerator


# Reading Audio file as source
# listening the audio file and store in audio_text variable
def audio_to_questions(split_file_list):
    qg = QuestionGenerator()

    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()
    r.energy_threshold = 300
    full_text = ""
    for audio_file_path in split_file_list:
        with sr.AudioFile(audio_file_path) as source:        
            audio_text = r.listen(source)
            try:
                # using google speech recognition
                text = r.recognize_google(audio_text,language='en-IN')        
                full_text += " " + text
                print("DONE with a part conversion = ",text)
                
            except Exception as e:
                print('Error in generation',e)
    print("full_text",full_text)    
    question_data = qg.generate(full_text,use_evaluator=True, num_questions=None, answer_style="multiple_choice")
    print('question conversion over')
    print(question_data)
    return question_data
            
        
        

