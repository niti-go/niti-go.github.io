---
title: Trying to Adapt Visual Anagrams to use Latent Diffusion
date: April 18, 2024
image: ./assets/blog-header-1.jpg
---

# Visual Anagrams

This semester in my Deep Learning course, I learned about the Visual Anagrams CVPR 2024 paper. The authors cleverly use diffusion models to generate optical illusions that can look like one image from one angle and a different image when rotated.

 (image of rotation and prompt)

They achieve this by feeding in two natural language prompts. During inference, they start with an image that is pure noise. They pass it through the diffusion model conditioned on the first prompt to predict the noise. At the same time, they also pass the rotated version of the image into the diffusion model conditioned on the second prompt. This gives them two noise estimates. They average the two noise estimates together and subtract that from the image. They repeat this for many timesteps to get the final result.

The final results are fun to look at and could have cool applications. For example, imagine a billboard in Times Square that 

passing in one image feed two natural language prompts in and receive an image out that satisfies one prompt one way and another prompt when rotated. 

The authors use pixel-space diffusion, which means the inputs to the denoiser network at every step is the entire 64x64x3 image data. It's more common nowadays to use latent diffusion, which is a type of diffusion model that uses a VAE to convert the image to and from a smaller 'latent' space where the denoiser network operates. This makes inference faster and allows you to generate larger, higher quality images.

However, the authors found that visual anagrams don't work in the latent space, because the latent space is not equivariant. That means that if you rotate an image's latent values, that doesn't necessarily mean you will exactly get the rotated image out. Rotations in the latent space don't correspond to rotations in the image space.

Unfortunately this means the authors were limited to using older models like DeepFloyd that support pixel-based diffusion, rather than newer models like Stable Diffusion which use latent diffusion and are more powerful.

# Can we adapt Visual Anagrams to use latent diffusion?

If it's possible to use latent diffusion to create visual anagrams, it could be much more useful