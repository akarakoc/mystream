package com.mystream.listener;

import com.mystream.dom.TextAnnotation;
import com.mystream.service.SequenceGeneratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.mapping.event.AbstractMongoEventListener;
import org.springframework.data.mongodb.core.mapping.event.BeforeConvertEvent;
import org.springframework.stereotype.Component;

@Component
public class TextAnnotationListener extends AbstractMongoEventListener<TextAnnotation> {

	private SequenceGeneratorService sequenceGenerator;

	@Autowired
	public TextAnnotationListener(SequenceGeneratorService sequenceGenerator) {
		this.sequenceGenerator = sequenceGenerator;
	}

	@Override
	public void onBeforeConvert(BeforeConvertEvent<TextAnnotation> event) {
//		if (event.getSource().getId() == null ) {
//			event.getSource().setId(sequenceGenerator.generateSequence(TextAnnotation.SEQUENCE_NAME));
//		}
	}



}
