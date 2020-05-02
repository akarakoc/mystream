package com.mystream.dom.selector;

import com.fasterxml.jackson.annotation.JsonTypeName;
import lombok.Getter;
import lombok.Setter;

@JsonTypeName("RangeSelector")
public class RangeSelector extends Selector {


	@Getter
	@Setter
	private XPathSelector startSelector;

	@Getter
	@Setter
	private XPathSelector endSelector;
}
