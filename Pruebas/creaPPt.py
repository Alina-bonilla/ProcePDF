import aspose.pydrawing as drawing
import aspose.slides as slides

# Applying the linence for Aspose.Slides
slidesLicense = slides.License()
slidesLicense.set_license("Aspose.Total.lic")

# Generate an empty presentation using Presentation class object
with slides.Presentation() as presentationObj:
    
    # Insert a Blank slide inside  the slides collection
    slide = presentationObj.slides.add_empty_slide(presentationObj.layout_slides.get_by_type(slides.SlideLayoutType.BLANK))

    # Add a Rectangle autoshape inside the newly added slide
    autoShape = slide.shapes.add_auto_shape(slides.ShapeType.RECTANGLE, 50, 150, 300, 0)

    # Fill the auto shape with color
    autoShape.fill_format.fill_type = slides.FillType.SOLID
    autoShape.fill_format.solid_fill_color.color = drawing.Color.green;

    # Add a text frame to insert some text inside the shape
    txtFrame = autoShape.add_text_frame("Welcome to Aspose Knowledgebase examples")

    # Apply the text related properties
    portionFormat = txtFrame.paragraphs[0].portions[0].portion_format
    portionFormat.fill_format.fill_type = slides.FillType.SOLID
    portionFormat.fill_format.solid_fill_color.color= drawing.Color.red
    portionFormat.font_bold = slides.NullableBool.TRUE
    portionFormat.font_italic = slides.NullableBool.TRUE
    portionFormat.font_height = 14

    # Save the generated presentation on the disk
    presentationObj.save("NewPresentation.pptx", slides.export.SaveFormat.PPTX) 