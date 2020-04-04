package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Document(collection = "TextAnnotation")
public class TextAnnotation implements Annotation  {

	@Transient
	public static final String SEQUENCE_NAME = "text_anno_seq";

	@Id
	@Getter
	@Setter
	private Long id;

	@Getter
	@Setter
	private String type;

	private List<MotivationEnum> motivation;

	private Annotator annotatedBy;

	private Serializer serializedBy;

	private List<Body> body;
}

