package com.mystream.anno;

import com.mystream.dom.Annotation;
import com.mystream.dom.AnnotationFactory;
import com.mystream.dom.TextAnnotation;
import com.mystream.repo.TextAnnotationRepository;
import com.mystream.service.AnnotationService;
import com.mystream.service.AnnotationServiceImpl;
import com.mystream.service.SequenceGeneratorService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

import javax.xml.soap.Text;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

@RestController
public class AnnotationRestController {

	@Autowired
	AnnotationService annotationService;

	@RequestMapping(name = "/annotateText", produces = "application/json", method= RequestMethod.POST)
	@ResponseBody
	public AnnotationResponse annotateText(@RequestBody AnnotationRequest request) throws Exception {

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
