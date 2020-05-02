package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("SvgSelector")
public class SvgSelector extends Selector {

	@Getter
	@Setter
	private String value;

}
