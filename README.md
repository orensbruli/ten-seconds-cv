# ten-seconds-cv

Hi!
My name is Esteban Martinena, a Software Engineer from Spain.
This is my resume, built with LaTeX, Pandoc, Docker...

## Download

Two formats are available. Plain first, then two-columns:

<p align="center">
    <a href="https://github.com/orensbruli/ten-seconds-cv/releases/latest/download/cv-esteban-martinena-plain.pdf">
        <img width="300" src="https://github.com/orensbruli/ten-seconds-cv/releases/latest/download/cv-esteban-martinena-plain-cover.png" alt="Plain CV">
    </a>
    <a href="https://github.com/orensbruli/ten-seconds-cv/releases/latest/download/cv-esteban-martinena-two-columns.pdf">
        <img width="300" src="https://github.com/orensbruli/ten-seconds-cv/releases/latest/download/cv-esteban-martinena-two-columns-cover.png" alt="Two-columns CV">
    </a>
</p>

- **Plain** — single-column, serif-based, reference-inspired design.
- **Two-columns** — sidebar layout with skill heatmap, based on AltaCV.

Both share the same data source (`data.md`). Format-specific LaTeX templates live under `latex/plain/` and `latex/two-columns/`.

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

## How?
Apart from using some nice LaTeX templates,
I've used [Pandoc](https://pandoc.org/) to convert the Markdown file to LaTeX.
This way I can write my resume in the data.md file, and then generate the LaTeX file and the PDF when I change it.

I've also used [Docker](https://www.docker.com/) to build the PDF file,
so I (or anyone else) can build it without installing anything else.

Data fields are shared across formats. Optional fields like `summary`, `expertise_groups`, and `featured_experiences` are used by the plain template, with fallbacks to the legacy fields for two-columns.

I've also created a simple Python script (`heatmap.py`) that generates an EPS heatmap of my skills, used by the two-columns format.

## GitHub Actions

### Docker image build
To avoid building the Docker image every time, a workflow builds it and pushes to GHCR.
It's only triggered when the Dockerfile or requirements.txt changes.

### PDF build
Runs on every push. It pulls the Docker image from GHCR and runs `make pdf-all` inside it,
which builds both formats. The resulting PDFs are uploaded as build artifacts and, on tag/release,
as release assets. The download links above point to the latest release assets.

## How to build locally?

```shell
docker run --rm -v $(pwd):/latex_content ghcr.io/orensbruli/latex-build:latest make pdf-all
```

Or for a single format:

```shell
docker run --rm -v $(pwd):/latex_content ghcr.io/orensbruli/latex-build:latest make pdf FORMAT=plain
docker run --rm -v $(pwd):/latex_content ghcr.io/orensbruli/latex-build:latest make pdf FORMAT=two-columns
```

Outputs `cv-esteban-martinena-{format}.pdf` and `cv-esteban-martinena-{format}-cover.png` in the current directory.

## References

The initial idea for this repo came from the following repositories:
1. [Ten Seconds CV](https://github.com/bitroniq/ten-seconds-cv)
2. [Carmine Spagnuolo's Twenty Seconds Curriculum Vitae](https://github.com/spagnuolocarmine/TwentySecondsCurriculumVitae-LaTex)
