package com.mystream.test;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.mystream.dom.Annotation;
import com.mystream.service.AnnotationService;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.test.context.junit4.SpringJUnit4ClassRunner;

import java.io.File;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

@SpringBootTest
@RunWith(SpringJUnit4ClassRunner.class)
public class AnnotationServiceTest {

	@Autowired
	private AnnotationService annotationService;

	@Autowired
	private ObjectMapper objectMapper = new ObjectMapper();

	ClassLoader classLoader = getClass().getClassLoader();

	private void test_save(String testDataFile){
		try{

			File file = new File(classLoader.getResource(testDataFile).getFile());

			Annotation anno = objectMapper.readValue(file, Annotation.class);
			annotationService.saveAnnotation(anno);

			Annotation foundAnno = annotationService.searchAnnotationWithCanonical(anno.getCanonical());

			assertThat(foundAnno != null );
			assertThat(foundAnno.getCanonical() == anno.getCanonical() );
			assertThat(foundAnno.getBody() != null );
			assertThat(foundAnno.getTarget() != null );

			annotationService.deleteAnnotation(foundAnno);

		}catch (Exception ex){
			System.out.println(ex.getMessage());
		}
	}

	@Test
	public void test_saveAnnotation_imageTarget() {

		test_save("test_save_imageTarget.json");

	}

	@Test
	public void test_saveAnnotation_textTarget() {

		test_save("test_save_textTarget.json");

	}

	@Test
	public void test_saveAnnotation_bodyWithVideo() {

		test_save("test_save_bodyWithVideo.json");

	}

	@Test
	public void test_saveAnnotation_bodyWithImage() {

		test_save("test_save_bodyWithImage.json");

	}

	@Test
	public void test_saveAnnotation_bodyWithText() {

		test_save("test_save_bodyWithText.json");

	}

	@Test
	public void test_searchAnnotationWithSource() {

		String test_source = "localhost:8080";
		List<Annotation> annoList = annotationService.searchAnnotationWithSource(test_source);

		assertThat(annoList != null );
		assertThat(annoList.size() > 0);

		for ( Annotation anno : annoList ) {
			assertThat(anno.getBody() != null );
			assertThat( anno.getTarget() != null );
		}
	}





}