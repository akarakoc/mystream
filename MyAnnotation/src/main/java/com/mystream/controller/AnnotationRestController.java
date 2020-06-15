package com.mystream.controller;

import com.mystream.dom.Constants;
import com.mystream.dom.selector.FragmentSelector;
import com.mystream.dom.selector.Selector;
import com.mystream.dom.selector.SelectorEnum;
import com.mystream.dom.Target;
import com.mystream.param.AnnotationRequest;
import com.mystream.param.AnnotationResponse;
import com.mystream.dom.Annotation;
import com.mystream.service.AnnotationService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class AnnotationRestController {

	@Autowired
	AnnotationService annotationService;

	@GetMapping("/annotation-javaconfig")
	public AnnotationResponse annotationWithJavaconfig(@RequestParam(required=false, defaultValue="World") String name) {
		System.out.println("==== in greeting ====");
		return new AnnotationResponse();
	}

	@RequestMapping(name = "/annotateText", produces = "application/json", method= RequestMethod.POST)
	@ResponseBody
	public AnnotationResponse annotateText(@RequestBody AnnotationRequest request) throws Exception {

		Annotation annotation = request.getAnno();
		annotation.setContext(Constants.ANNOTATION_CONTEXT_URI);

		Target target = annotation.getTarget();
		for ( Selector selector: target.getSelector()) {
			if(target.getSelector().equals(SelectorEnum.FragmentSelector)){
				((FragmentSelector)target.getSelector()).setConformsTo(Constants.SELECTOR_FRAGMENT_CONFORMS_TO);
			}
		}


		Annotation anno = annotationService.saveAnnotation(request.getAnno());
		AnnotationResponse response = new AnnotationResponse();
		response.getResponse().put("annoList", anno );
		return response;

	}

	@RequestMapping(name = "/searchAnnotation", produces = "application/json", method= RequestMethod.GET)
	@ResponseBody
	public AnnotationResponse searchAnnotation(@RequestParam(name = "source") String source){

		List<Annotation> annoList = annotationService.searchAnnotationWithSource(source);
		AnnotationResponse response = new AnnotationResponse();
		response.getResponse().put("annoList", annoList );
		return response;
	}
}
