package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("TextQuoteSelector")
public class TextQuoteSelector extends Selector {

	//	For TextQuoteSelector
	@Getter
	@Setter
	private String exact;

	@Getter
	@Setter
	private String prefix;

	@Getter
	@Setter
	private String suffix;
}
