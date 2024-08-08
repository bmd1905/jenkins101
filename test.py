
# optimizer_1: CLIP
# optimizer_2: Decoder

# Multitask learning
for image, caption, label in trainloader():
    # image: [batch_size, 224x224x3]
    # caption: [bs, dim]
    # label: [bs, dim]

    # Stage 1: train CLIP (image, label)
    image_ft = clip_model.encode_image(image) # [bs, 512]
    text_ft = clip_model.encode_text(label) # [bs, 512]
    
    # Cosine similarity
    sim = torch.cosine_similarity(image_ft, text_ft, dim=-1) # [bs]
    loss = criterion(sim, label) # loss
    
    loss.backward()
    optimizer_1.step()
    optimizer_1.zero_grad()
    
    # Stage 2: train CLIP (image, caption)
    image_ft = clip_model.encode_image(image) # [bs, 512]
    text_ft = clip_model.encode_text(label) # [bs, 512]
    
    fusion_ft = (image_ft + text_ft) / 2
    
    # Decoder
    output  = decoder(caption, fusion_ft) # [bs, vocab_size]

    loss.backward()
    optimizer_2.step()
    optimizer_2.zero_grad()
    
    
    
