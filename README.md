# POEditor-Android-Translator
Script to translate android strings.xml to a csv so that it can be imported into [POEditor](https://poeditor.com/) and then translate the identical csv with the translations back into a strings.xml file

## Problem I had

Below is a snippet from a strings.xml file 
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="name_dog">Dog</string>
    <string name="name_cat">Cat</string>
    <string name="name_prompt">What is your name?</string>
    <string name="age_prompt">Please enter your age.</string>
    <string-array name="rooms">
        <item>Bathroom</item>
        <item>Kitchen</item>
    </string-array>
</resources>
```

Now importing this into [POEditor](https://poeditor.com/) yields the following

![Alt text](/screenshots/poeditorscreenshot1.png "POEditor Screenshot")

Which is probably not what you want to translate

## Solution I made

Execute the translate script with the translate option 

```
python translate.py -o translate
```

and then enter the file name when prompted

```
File name(Or absolute path to file):
strings.xml
```

and two csv files should now be present in the directory one to be 
imported into [POEditor](https://poeditor.com/) which is the values.csv
and the other to be used to rebuild the strings xml with the translation -
names.csv

Now let's import the values.csv into POEditor

We get the actually values and **note** [POEditor](https://poeditor.com/) **does not support the string 
array tags** but we still got those imported as well so that should 
be a plus!

![Alt text](/screenshots/poeditorscreenshot2.png "POEditor Screenshot Import")

### Rebuilding the Strings XML file

Let's do that!

I used POEditor's awesome automatic translation feature and translated 
the terms and got this

![Alt text](/screenshots/poeditorscreenshot3.png "POEditor Screenshot translation")

Now let's export this as a csv, the exported data looks like this

```
Dog,Perro
Cat,Gato
"What is your name?","¿Cuál es su nombre?"
"Please enter your age.","Por favor, introduzca su edad."
Bathroom,Baño
Kitchen,Cocina
```

Now we build back our strings.xml with the following command 

```
python translate.py -o build
```

and enter the file names when prompted

```
File name for csv containing string names(Or absolute path to file):
names.csv
File name for csv containing translation(Or absolute path to file):
translation.csv
Resulting strings stored in output.xml
```

and voila we have the result in the output.xml file that looks like

```
<?xml version="1.0" encoding="utf-8"?>
<resources>
	<string name="name_dog">Perro</string>
	<string name="name_cat">Gato</string>
	<string name="name_prompt">"¿Cuál es su nombre?"</string>
	<string name="age_prompt">"Por favor, introduzca su edad."</string>
	<string-array name="rooms">
		<item>Baño</item>
		<item>Cocina</item></string-array>
</resources>
```

As you see the string array isn't perfect lol but it's correct

### Hope this helps someone else

Feel free to open issues if you come across any and I'll try and address

All suitable contributions welcome

## Contributing

I opened a couple issues for these feel free to tackle them 

* Need to be able to handle plurals
* Formatting for the last tag of the string array
* More test cases
