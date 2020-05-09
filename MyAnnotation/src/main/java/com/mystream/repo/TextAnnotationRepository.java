package com.mystream.repo;

import com.mystream.dom.TextAnnotation;
import org.springframework.data.mongodb.repository.MongoRepository;
import org.springframework.data.mongodb.repository.Query;
import org.springframework.stereotype.Repository;

import java.util.List;

public interface TextAnnotationRepository extends MongoRepository<TextAnnotation, Long> {

	@Query("{id:'?0'}")
	public TextAnnotation findByID(Long id);

	public List<TextAnnotation> findAll();

	public List<TextAnnotation> findByTarget_Source(String source);

}
