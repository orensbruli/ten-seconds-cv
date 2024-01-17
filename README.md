# ten-seconds-cv

Hi!
My name is Esteban Martinena, a Software Engineer from Spain. 
This is my resume, built with LaTeX, Pandoc, Docker...

## Why?
As many other developers, I really hate to write or update my resume.
I've tried many different approaches, but I've never been satisfied with the result.
Including new information, changing the format, or even modifying the order of the sections was always a pain.

At some point, I decided to write my resume in LaTeX,
but the more important thing was to automate the process of building the PDF file
and extracting the information from a single source of truth.

Also, I wanted to have a repository with my resume, so I could track the changes and share it with others, and
at the same time show some of my skills as DevOps and Software Engineer here.

So, not only the PDF generated in this repository is my resume, but also the repository itself.

As you can see in the commit history, it's a work in progress that started recently.
So don't be too harsh with me :) It's NOT yet on version 1.0.

## How?
Apart from using some nice LaTeX templates,
I've used [Pandoc](https://pandoc.org/) to convert the Markdown file to LaTeX.
This way I can write my resume in the data.md file, and then generate the LaTeX file and the PDF when I change it.

I've also used [Docker](https://www.docker.com/) to build the PDF file,
so I (or anyone else) can build it without installing anything else.

At some point, I also decided I wanted a more visual to show my skills.
Having the GitHub heatmap in mind, I decided to create a heatmap of my skills.
I have created a simple Python script that generates eps file with the heatmap, and then I include it in the LaTeX file.

## GitHub actions
I have created some GitHub actions to automate the process of building the PDF file.

### Docker image build
To avoid building the docker image every time, I've created a GitHub action that builds the image and pushes it to GHCR.
It's only triggered when the Dockerfile or requirements.txt changes.

### PDF build
This is the main action.
It is run on every push, and it uses the docker image built in the previous step to build the PDF file.
After building the PDF file, it's uploaded as an artifact, so it can be downloaded from the Actions tab.

On release, the PDF file is also uploaded as a release asset.

## How to build the PDF file locally?

Clone this repository and run the following command in the root directory of the repository:
```shell
docker build -t latex-cv .
docker run -v $(pwd):/latex_content --name latex-container latex-cv /bin/sh -c "make pdf"
docker cp latex-container:/latex_content/cv-piotr-kowalski.pdf output.pdf
docker remove /latex-container

# If you don't need to copy the PDF file from the container, you can use this command instead
docker run -v $(pwd):/latex_content latex-cv /bin/bash -c "make pdf"
```



## References

The initial idea for this repo came from the following repositories:
1. [Ten Seconds CV](https://github.com/bitroniq/ten-seconds-cv)
2. [Carmine Spagnuolo's Twenty Seconds Curriculum Vitae](https://github.com/spagnuolocarmine/TwentySecondsCurriculumVitae-LaTex)
3. [Harsh Gadgil opensorcer/Data-Engineer-Resume-LaTeX](https://github.com/opensorceror/Data-Engineer-Resume-LaTeX)
