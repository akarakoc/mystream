package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("TextPositionSelector")
public class TextPositionSelector extends Selector{

	//	For TextPositionSelector
	@Getter
	@Setter
	private Integer start;

	@Getter
	@Setter
	private Integer end;
}
