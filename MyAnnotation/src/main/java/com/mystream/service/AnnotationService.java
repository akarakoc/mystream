package com.mystream.service;

import com.mystream.dom.TextAnnotation;
import org.springframework.stereotype.Service;


public interface AnnotationService {

	public TextAnnotation saveTextAnnotation(TextAnnotation anno);
}
