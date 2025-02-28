package com.badminton.highlight_generator;

import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/video")
public class VideoController {

    @GetMapping("/process")
    public String processVideo(@RequestParam String url) {
        return "Processing video from URL: " + url;
    }
}
