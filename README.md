## DictToCSV
---
This is a small project that utilizes the Oxford Dictionary API in order to create a TSV of vocabulary words and their definitions. Definitions are created by listing up to two synonyms and then up to two definitions. 

This project took three hours, so bugs are to be expected


### How to use
---
1. Modify <code> settings.json </code> ; the most important parts are in modifying the <code> apiid </code> and <code> apikey </code> fields. 
2. Have a list of words. The list of words should be in a single file, separated by line breaks.
3. Modify <code> settings.json </code> so that the <code> input_file</code> refers to the file in step 2
4. Execute <code> python run.py </code> in terminal


There are other mandatory parameters that can be used in the <code> settings.json </code> file. These are the <code> words_per_file </code> and <code> output_folder </code> fields. <code> words_per_file </code> dictates how many words go into each file and <code> output_folder </code> refers to teh directory where the output files go.