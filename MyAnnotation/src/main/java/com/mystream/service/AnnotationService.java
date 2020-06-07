package com.mystream.service;

import com.mystream.dom.Annotation;
import org.springframework.stereotype.Service;

import java.util.List;

public interface AnnotationService {

	public Annotation saveAnnotation(Annotation anno);
	public List<Annotation> searchAnnotation();
	public List<Annotation> searchAnnotationWithSource( String source);
	public Annotation searchAnnotationWithCanonical( String canonical);
	public void deleteAnnotation( Annotation anno);

	}
