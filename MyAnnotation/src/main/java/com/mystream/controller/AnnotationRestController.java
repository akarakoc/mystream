package com.mystream.controller;

import com.mystream.dom.Constants;
import com.mystream.dom.Selector;
import com.mystream.dom.Target;
import com.mystream.dom.TypeEnum;
import com.mystream.param.AnnotationRequest;
import com.mystream.param.AnnotationResponse;
import com.mystream.dom.TextAnnotation;
import com.mystream.service.AnnotationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class AnnotationRestController {

	@Autowired
	AnnotationService annotationService;

	@CrossOrigin(origins = "http://127.0.0.1:8000/")
	@RequestMapping(name = "/annotateText", produces = "application/json", method= RequestMethod.POST)
	@ResponseBody
	public AnnotationResponse annotateText(@RequestBody AnnotationRequest request) throws Exception {

		TextAnnotation annotation = request.getTextAnno();
		annotation.setContext(Constants.ANNOTATION_CONTEXT_URI);

		for ( Target target : annotation.getTarget()) {
			if(target.getSelector().equals(TypeEnum.FragmentSelector))
				target.getSelector().setConformsTo(Constants.SELECTOR_FRAGMENT_CONFORMS_TO);
		}

		TextAnnotation anno = annotationService.saveTextAnnotation(request.getTextAnno());
		AnnotationResponse response = new AnnotationResponse();
		response.getResponse().put("annoList", anno );
		return response;

	}

	@RequestMapping(name = "/searchAnnotation", produces = "application/json", method= RequestMethod.GET)
	@ResponseBody
	public AnnotationResponse searchAnnotation(){

		List<TextAnnotation> annoList = annotationService.searchAnnotation();
		AnnotationResponse response = new AnnotationResponse();
		response.getResponse().put("annoList", annoList );
		return response;
	}
}
