package com.mystream.service;

import com.mystream.dom.Annotation;
import com.mystream.dom.Annotation;
import com.mystream.repo.AnnotationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class AnnotationServiceImpl implements AnnotationService {

	@Autowired
	AnnotationRepository annoRepository;

	@Override
	public Annotation saveAnnotation(Annotation anno){

		Annotation current = annoRepository.findByCanonical(anno.getCanonical());
		if(current != null){
			current.setBody(anno.getBody());
			return annoRepository.save(current);
		}
		return annoRepository.save(anno);
	}

	@Override
	public List<Annotation> searchAnnotation(){
		return annoRepository.findAll();
	}

	@Override
	public List<Annotation> searchAnnotationWithSource( String source){
		return annoRepository.findByTarget_SourceLike(source);
	}

}
