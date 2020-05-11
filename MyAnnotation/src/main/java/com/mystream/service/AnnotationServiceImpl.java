package com.mystream.service;

import com.mystream.dom.TextAnnotation;
import com.mystream.repo.TextAnnotationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AnnotationServiceImpl implements AnnotationService {

	@Autowired
	TextAnnotationRepository textRepository;

	@Override
	public TextAnnotation saveTextAnnotation(TextAnnotation anno){

		TextAnnotation current = textRepository.findByCanonical(anno.getCanonical());
		if(current != null){
			current.setBody(anno.getBody());
			return textRepository.save(current);
		}
		return textRepository.save(anno);
	}

	@Override
	public List<TextAnnotation> searchAnnotation(){
		return textRepository.findAll();
	}

	@Override
	public List<TextAnnotation> searchAnnotationWithSource( String source){
		return textRepository.findByTarget_Source(source);
	}

}
