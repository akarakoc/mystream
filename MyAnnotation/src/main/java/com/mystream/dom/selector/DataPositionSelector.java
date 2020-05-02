package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;
@JsonTypeName("DataPositionSelector")
public class DataPositionSelector extends Selector {

	@Getter
	@Setter
	private Integer start;

	@Getter
	@Setter
	private Integer end;
}
