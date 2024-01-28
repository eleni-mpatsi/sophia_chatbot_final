Disclaimers :
- In the time span of the assignment, a very specific error kept appearing (GraphComponentException: Error running graph component for node train_TEDPolicy0), and took most of the time available. After googling it, it seems that many people had to deal with it and kept asking in the rasa forum, but none of them had an answer. That is the reason why i had to keep things simple in order to create a complete result.
- The outputs of the bot are in bold.
- The screenshots of the policy experiments that are referenced below, are inside the folder /rasa_example_dialogs

**1 . Forms**
<br>

Changes- Updates in the chatbot scenarios
<br>
<br>

A. Adding a name form when the user wants to call someone

<br>
<br>

Your input ->  please call someone

**What is the first name of this person?**

Your input ->  el

**There is not such a short name in your contacts.**
**What is the first name of this person?**

Your input ->  el###

**Are you sure 'el###' is correct? This did not sound right.**
**What is the first name of this person?**

Your input ->  eleni

**What is the last name of this person?**

Your input ->  are you a bot?

**I am a bot, powered by Rasa.**
**What is the last name of this person?**

Your input ->  mpatsi

**Ok. Thanks!**
**I will call eleni mpatsi later!**


To create this dialog, two stories and three rules were created (also the domain.yml file was updated accordingly). 1 story was for the description of how the form will work and 1 of how the bot will handle an interruption and continue with the form. The rules for this form were: 1 for activation of the form, 1 for the submission and 1 for the interruption, respectively. The ways that the bot will validate and handle any interruptions are defined in the actions.py. Specifically, for the name form , the user asks the bot to call someone and the bot should retrieve the info of this person, before calling , name and surname - this was obtained from the rasa example given for the forms -. 
The validation of these two slots regards 2 requirements for the input: 
  1. not to have other non-alphabetic characters (in our case, as an intercom assistant for the biker, the answer is "this did not sound right") 
  2. not to have less than 3 characters

As for the interruption part, this is defined again in actions.py, inside the validation class, where some chitchat intents are determined, like the bot_challenge. Inside the class, the bot is set to send back a none slot and keep asking for the slot, if another intent interrupts the completion of the form.

<br>
<br>
<br>
B. Adding a music form when the user wants to call someone
<br>
<br>


Your input ->  hey

**Hey! How are you?**

Your input ->  change the song

**What is the title?**

Your input ->  lov

**I'm sorry, but I don't recognize that song. Please choose a song from our list.**
**What is the title?**

Your input ->  love me 

**Great choice!**
**Who is the artist?**

Your input ->  Where is the closest gas station?

**The nearest gas station is []**
**Who is the artist?**

Your input ->  morandi

**OK!**
**That's a great choice. love me by morandi coming right away.**


Same as the name form, the music form gets activated in a similar way, but for puting a song with a specific title and by a specific artist. I followed the same tactic for the stories, rules and domain but for the validation of the input, i put a small list of the songs and artists, just for demostration reasons. The bot can also handle the chitchat case, as it is shown above in the dialogue.

<br>
<br>
<br>
C. Optional! -> using an api key for latest news (get the top 2 articles)
<br>
<br>
<br>
Your input ->  what is happening in the world?      

**World's Largest Cruise Ship Sets Sail Raising Methane Emission Concerns - NDTV
The crusie ship, Icon of the Seas, is built to run on liquefied natural gas
New York: The world's largest cruise ship is set for its maiden voyage on Saturday, but environmental groups are concerned… [+3443 chars]
Fuel tanker's crew struggle to contain fire after Houthi missile attack - Financial Times
Crew members were battling to control a fire on the Marlin Luanda on Saturday, 18 hours after the tanker was struck by a Houthi missile in the Gulf of Aden.
The fire on the vessel has made it the mo… [+3715 chars]**

I wanted to try using an api key and one of the free ones was the the NewsApi. The bot gets back to the user the top 2 articles. I really wanted to find an api key for travel advice in order to update my previous dialogs, but there was no time for that, so i will check this out as soon as all the assignments are done :) 

<br>
<br>
<br>
D. Optional! -> Adding a default fallback action in actions.py 
<br>
<br>
<br>
Your input ->  are you a bot ?

**I am a bot, powered by Rasa.**

Your input ->  i am not in the mood for food

**please rephrase that**

Your input ->  why

**please rephrase that**

When I tried to experiment with different policies, i tried working with all 3 policies but use 2 options for each policy each time : the default and another one , in which i change the parameter values. Since i did not notice significant differences , i tried using the default fallback action, to see if it was going to change the behavior of the bot in different scenarios of the same policy. This did not work either.
<br>
<br>
<br>
**2. Rasa Policies**
<br>
<br>
<br>
Brief Description of different parameters for each policy . I will provide pictures of the dialogs labeled with the changed values of the parameters. The example-dialogs will be updated in a file called images.

Since no significant difference was noticed between the default and other parameters of the policies (you can check them out as comments in the config.yml) when all three simultaneously used , these are some observations: 

- RulePolicy :  I changed the core_fallback_threshold from 0.3 (default) to 0.8 . When an action confidence is below the threshold, Rasa  runs the default fallback action---> The 0.8 value made the performance of the bot a bit worse by answering more often the fallback message "please rephrase that" even in intents that the model was trained with in the stories , like "hey" and "I am sad". So, in this case , the default Rule Policy did better and will be used for all other experiments from now on.

- MemoizationPolicy : For this policy, max_history= 3 and =5 was tested. The max_history number is the number of turns of the conversation the bot will take into account . In this case, there was no difference between the two policies and as it can be seen in the images, both of them had a hard time handling the input "I’m considering travelling to [] for a road trip. What do you think?", which was not on the stories exactly like this, but the bot usually can handle paraphrashes of the input in the stories. For some reason, this message activated the name_form.

- TEDPolicy: For this policy , these two options were tested:

a. max_history: 5, epochs: 50, constrain_similarities: true

b. max_history: 6, epochs: 150,  (number_of_transformer_layers:text: 3, action_text: 3, label_action_text: 3, dialogue: 3), (transformer_size: text: 192, action_text: 192, label_action_text: 192, dialogue: 192), connection_density: 0.3, constrain_similarities: false, model_confidence: softmax

Both policies seemed to do very good and not a difference was captured, so i decided to go with the first option.

<br>
<br>

Experimenting more...
<br>
<br>
<br>
A. Using only Rule Policy
<br>
<br>
<br>

Your input ->  hey

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**2024-01-28 16:57:22 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender 'a07397b4857b4086a0333f030812a4ca'.**

**please rephrase that**

**please rephrase that**

Your input ->  please call someone 

**2024-01-28 16:57:26 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender 'a07397b4857b4086a0333f030812a4ca'.**

Your input ->  change the song

**2024-01-28 16:57:38 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender 'a07397b4857b4086a0333f030812a4ca'.**

Using the RulePolicy only is surely not the way to go. The bot kept using the default fallback message until it stopped predicting

<br>
<br>
<br>
B. Using only Memoization Policy
<br>
<br>
<br>

Your input ->  hey

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**2024-01-28 16:44:51 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '27540d3e6c7f4a878d8d60332151b299'.**

**please rephrase that**

**please rephrase that**

Your input ->  are you a bot?

**2024-01-28 16:44:59 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '27540d3e6c7f4a878d8d60332151b299'.**

Your input ->  please call someone

**2024-01-28 16:45:15 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '27540d3e6c7f4a878d8d60332151b299'.**

Your input ->  cu

**2024-01-28 16:46:28 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '27540d3e6c7f4a878d8d60332151b299'.**

Using only the MemoizationPolicy resulted the same way as using only the rule policy.

<br>
<br>
<br>
C. Using only TED Policy 
<br>
<br>
<br>

2024-01-28 16:48:47 ERROR    rasa.engine.graph  - Error running graph component for node schema_validator.
InvalidDomain: You have defined a form action, but have not added the 'RulePolicy' to your policy ensemble. Either remove all forms from your domain or add the 'RulePolicy' to your policy configuration.

The bot won't even let me use only the TEDPolicy alone and raises an error.


<br>
<br>
<br>
D. Memoization + Rule Policy
<br>
<br>
<br>

Your input ->  hey

**Hey! How are you?**

Your input ->  are you a bot ?

**I am a bot, powered by Rasa.**

Your input ->  please call someone

**What is the first name of this person?**

Your input ->  eleni

**What is the last name of this person?**

Your input ->  are you really a bot ?

**I am a bot, powered by Rasa.**
**What is the last name of this person?**

Your input ->  mpatsi

**Ok. Thanks!**
**I will call eleni mpatsi later!**

Your input ->  ...

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**please rephrase that**

**2024-01-28 17:03:34 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '8163c83f51094a7c8f99962be01cdacd'.**

**please rephrase that**

**please rephrase that**

Your input ->  what is my current location?

**2024-01-28 17:03:55 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '8163c83f51094a7c8f99962be01cdacd'.**

Your input ->  hello

**2024-01-28 17:04:03 WARNING  rasa.core.processor  - Circuit breaker tripped. Stopped predicting more actions for sender '8163c83f51094a7c8f99962be01cdacd'.**


The combination of Memoization + Rule Policy appeared initially ok, until the intent "silence" appeared, in which the bot was actually trained in the stories, but still could not handle it correctly and started the "please rephrase that" poem, before totaly stopping predicting.

<br>
<br>
<br>
E. Ted Policy + Rule Policy 
<br>
<br>
<br>

Your input ->  hey

**Hey! How are you?**

Your input ->  are you a bot?

**I am a bot, powered by Rasa.**

Your input ->  please call someone

**What is the first name of this person?**

Your input ->  eleni

**What is the last name of this person?**

Your input ->  are you really a bot?

**I am a bot, powered by Rasa.**
**What is the last name of this person?**

Your input ->  mpatsi

**Ok. Thanks!**
**I will call eleni mpatsi later!**

Your input ->  ...

**Can i help you with anything else?**

Your input ->  what is my current location?

**You are in Florence.**

Your input ->  i am sad but i am happy

**Here is something to cheer you up:
Image: https://i.imgur.com/nGF1K8f.jpg**

Your input ->  perfect

**Great, carry on!**

This is the best combination so far, where the bot managed to handle every intent.

<br>
<br>
<br>
F. Memoization + ted policy
<br>
<br>
<br>

2024-01-28 17:17:27 ERROR    rasa.engine.graph  - Error running graph component for node schema_validator.
InvalidDomain: You have defined a form action, but have not added the 'RulePolicy' to your policy ensemble. Either remove all forms from your domain or add the 'RulePolicy' to your policy configuration.

<br>
This combination did not work.

<br>
<br>
<br>

In conclusion, the experimentation with different policies and their variation was interesting and i am sure that by diving deeper, the difference between the different parameters will be more obvious. However, in our case, the default values worked just fine and produced the best outcome possible. The optimal combination used was all 3 default policies along with the pipeline that rasa gives in its examples for forms -->                                                                                                                 pipeline:
- name: WhitespaceTokenizer
- name: RegexFeaturizer
- name: LexicalSyntacticFeaturizer
- name: CountVectorsFeaturizer
- name: CountVectorsFeaturizer
  analyzer: char_wb
  min_ngram: 2
  max_ngram: 4
- name: DIETClassifier
  epochs: 100
  constrain_similarities: true
  model_confidence: softmax

<br>
<br>
<br>
<br>
The test case of all the elements referenced above is presented below:
<br>
<br>
Your input ->  hey

**Hey! How are you?**

Your input ->  please call someone

**What is the first name of this person?**

Your input ->  el

**There is not such a short name in your contacts.**
**What is the first name of this person?**

Your input ->  el%%%

**Are you sure 'el%%%' is correct? This did not sound right.**
**What is the first name of this person?**

Your input ->  eleni

**What is the last name of this person?**

Your input ->  are you a bot?

**I am a bot, powered by Rasa.**
**What is the last name of this person?**

Your input ->  mpatsi

**Ok. Thanks!**
**I will call eleni mpatsi later!**

Your input ->  ...

**Can i help you with anything else?**

Your input ->  change the song

**What is the title?**

Your input ->  love her

**I'm sorry, but I don't recognize that song. Please choose a song from our list.**
**What is the title?**

Your input ->  Where is the closest gas station?

**The nearest gas station is []**
**What is the title?**

Your input ->  love me

**Great choice!**
**Who is the artist?**

Your input ->  morandi

**OK!**

**That's a great choice. love me by morandi coming right away.**


