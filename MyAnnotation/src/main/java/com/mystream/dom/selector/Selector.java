package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import lombok.Getter;
import lombok.Setter;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;
import com.fasterxml.jackson.annotation.JsonTypeInfo.As;


@JsonTypeInfo(use=JsonTypeInfo.Id.NAME, include = As.PROPERTY, property="type", visible=true )
@JsonSubTypes({   @JsonSubTypes.Type(value = DataPositionSelector.class, name = "DataPositionSelector"),
				  @JsonSubTypes.Type(value = FragmentSelector.class, name = "FragmentSelector"),
				  @JsonSubTypes.Type(value = RangeSelector.class, name = "RangeSelector"),
				  @JsonSubTypes.Type(value = SvgSelector.class, name = "SvgSelector"),
				  @JsonSubTypes.Type(value = TextQuoteSelector.class, name = "TextQuoteSelector"),
				  @JsonSubTypes.Type(value = TextPositionSelector.class, name = "TextPositionSelector"),
				  @JsonSubTypes.Type(value = XPathSelector.class, name = "XPathSelector")
			  })
@Document(collection = "Selector")
public class Selector {

	@Id
	@Getter
	@Setter
	@JsonInclude
	private String id;

	@Getter
	@Setter
	@JsonProperty("type")
	@JsonInclude
	private SelectorEnum type;


	@Getter
	@Setter
	private Selector refinedBy;



}
