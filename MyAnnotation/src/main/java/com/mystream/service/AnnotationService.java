package com.mystream.service;

import com.mystream.dom.TextAnnotation;
import org.springframework.stereotype.Service;

import java.util.List;

public interface AnnotationService {

	public TextAnnotation saveTextAnnotation(TextAnnotation anno);
	public List<TextAnnotation> searchAnnotation();
}
