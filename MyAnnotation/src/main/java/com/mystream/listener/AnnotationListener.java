package com.mystream.listener;

import com.mystream.dom.Annotation;
import com.mystream.service.SequenceGeneratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import org.springframework.data.mongodb.core.mapping.event.BeforeConvertEvent;
import org.springframework.stereotype.Component;

@Component
public class AnnotationListener extends AbstractMongoEventListener<Annotation> {

	private SequenceGeneratorService sequenceGenerator;

	@Autowired
	public AnnotationListener(SequenceGeneratorService sequenceGenerator) {
		this.sequenceGenerator = sequenceGenerator;
	}

	@Override
	public void onBeforeConvert(BeforeConvertEvent<Annotation> event) {
//		if (event.getSource().getId() == null ) {
//			event.getSource().setId(sequenceGenerator.generateSequence(Annotation.SEQUENCE_NAME));
//		}
	}



}
