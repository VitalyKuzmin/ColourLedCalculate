
from docx import *
import docx

def create_word(name,images):
    # Default set of relationshipships - the minimum components of a document
    relationships = relationshiplist()

    # Make a new document tree - this is the main part of a Word document
    document = newdocument()

    # This xpath location is where most interesting content lives
    body = document.xpath('/w:document/w:body', namespaces=nsprefixes)[0]

    # Add an image
    def add_image(image,relationships):
        relationships, picpara = picture(relationships, image,
                                     'description',pixelwidth=200,pixelheight=200)
        body.append(picpara)

    for image in images:
        add_image(image,relationships)

    # Create our properties, contenttypes, and other support files
    title    = 'Python docx demo'
    subject  = 'A practical example of making docx from Python'
    creator  = 'Mike MacCana'
    keywords = ['python', 'Office Open XML', 'Word']

    coreprops = coreproperties(title=title, subject=subject, creator=creator,
                               keywords=keywords)
    appprops = docx.appproperties()
    contenttypes = docx.contenttypes()
    websettings = docx.websettings()
    wordrelationships = docx.wordrelationships(relationships)

    # Save our document
    savedocx(document, coreprops, appprops, contenttypes, websettings,
             wordrelationships, name)





