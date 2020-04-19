package com.mystream.dom;

public class AnnotationFactory {

	public Annotation createAnnotation(Annotation anno){

		if(anno instanceof TextAnnotation)
			return new TextAnnotation();
		else if(anno instanceof ImageAnnotation)
			return new ImageAnnotation();

		return null;
	}

	private TextAnnotation createTextAnnotation(TextAnnotation textAnno){

		return null;
	}
}
