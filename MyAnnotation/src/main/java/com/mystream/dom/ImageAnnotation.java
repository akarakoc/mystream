package com.mystream.dom;

import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "ImageAnnotation")
public class ImageAnnotation implements Annotation {

	@Transient
	public static final String SEQUENCE_NAME = "img_anno_seq";

	@Id
	@Getter
	@Setter
	private Long id;
}