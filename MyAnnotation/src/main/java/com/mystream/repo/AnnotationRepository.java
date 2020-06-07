package com.mystream.repo;

import com.mystream.dom.Annotation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

public interface AnnotationRepository extends MongoRepository<Annotation, Long> {

	public Annotation findByCanonical(String canonical);

	public List<Annotation> findAll();

	public List<Annotation> findByTarget_SourceLike(String source);



}
