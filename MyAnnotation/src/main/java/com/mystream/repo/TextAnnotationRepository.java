package com.mystream.repo;

import com.mystream.dom.TextAnnotation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

public interface TextAnnotationRepository extends MongoRepository<TextAnnotation, Long> {

	public TextAnnotation findByCanonical(String canonical);

	public List<TextAnnotation> findAll();

	public List<TextAnnotation> findByTarget_SourceLike(String source);



}
