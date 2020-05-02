package com.mystream.dom;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.mongodb.lang.NonNull;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;
import org.springframework.data.mongodb.core.mapping.Field;

import javax.persistence.OneToMany;
import java.net.URI;
import java.util.List;


@Document(collection = "TextAnnotation")
public class TextAnnotation implements Annotation  {

	@Transient
	public static final String SEQUENCE_NAME = "text_anno_seq";

	@Getter
	@Setter
	@NonNull
	@Field("id")
	@JsonProperty("@id")
	private String id;

	@Getter
	@Setter
	@OneToMany
	@Field("context")
	@JsonProperty("@context")
	private String context;

	@Getter
	@Setter
	@OneToMany
	@Field("type")
	@JsonProperty("@type")
	private List<TypeEnum> type;

	@Getter
	@Setter
	private MotivationEnum motivation;

	@Getter
	@Setter
	private Annotator annotatedBy;

	@Getter
	@Setter
	private Serializer serializedBy;

	/**
	 * Annotations have 0 or more bodies.
	 */
	@Getter
	@Setter
	private List<Body> body;

	/**
	 * Annotations have 1 or more bodies.
	 */
	@Getter
	@Setter
	@NonNull
	private Target target;

	@Getter
	@Setter
	private String canonical;









}

