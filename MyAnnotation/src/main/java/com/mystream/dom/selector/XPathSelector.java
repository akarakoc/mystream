package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("XPathSelector")
public class XPathSelector extends Selector {

	//	For XPathSelector
	@Getter
	@Setter
	private String value;
}
