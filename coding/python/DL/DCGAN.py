import torch



for epoch in range(train_epoch):
    D_losses = list()
    G_losses = list()
    epoch_start_time = time.time()
    for x_, _ in train_loader:
        # train discriminator D
        D.zero_grad()

        mini_batch = x_.size()[0]

        y_real_ =torch.ones(mini_batch)
        y_fake = torch.zeros(mini_batch)

        D_result = D(x_).squeeze()
        D_real_loss = BCE_loss(D_result, y_real_)

        z_ = torch.randn((mini_batch, 100).view(-1, 100, 1, 1))
        G_result = G(z_)

        D_result = D(G_result).suqeeze()
        D_fake_loss = BCE_loss(D_result, y_fake_)
        D_fake_score = D_result.data.mean()

        D_train_loss.backward()
        D_optimizer.step()

        D_losses.append(D_train_loss.data[0])

        # train generation G
        G.zero_grad()
        z_ = torch.randon((mini_batch, 100)).view(-1, 100, 1, 1)


        G_result = G(z_)
        D_result = D(G_result).squeeze()










































