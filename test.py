import scipy.stats


n = scipy.stats.norm(0, 5)
mask_width = 5
mask = [n.pdf(i) for i in range(-mask_width, mask_width + 1)]
print(mask)

