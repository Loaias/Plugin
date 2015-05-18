# -*- coding: utf8 -*-

from core import G
import material
import image
import image_operations as imgop
import projection
import mh


def my_render(settings=None):
    if settings is None:
        settings = {'AA': True, 'lightmapSSS': False, 'scene': G.app.scene, 'dimensions': (230, 230)}

    if settings['lightmapSSS']:
        human = G.app.selectedHuman
        material_backup = material.Material(human.material)

        diffuse = imgop.Image(data=human.material.diffuseTexture)
        lmap = projection.mapSceneLighting(settings['scene'], border=human.material.sssRScale)
        lmapG = imgop.blurred(lmap, human.material.sssGScale, 13)
        lmapR = imgop.blurred(lmap, human.material.sssRScale, 13)
        lmap = imgop.compose([lmapR, lmapG, lmap])

        if not diffuse.isEmpty:
            lmap = imgop.resized(lmap, diffuse.width, diffuse.height, filter=image.FILTER_BILINEAR)
            lmap = imgop.multiply(lmap, diffuse)
            lmap.sourcePath = "Internal_Renderer_Lightmap_SSS_Texture"

        human.material.diffuseTexture = lmap
        human.configureShading(diffuse=True)
        human.shadeless = True

    if not mh.hasRenderToRenderbuffer():
        img = mh.grabScreen(0, 0, G.windowWidth, G.windowHeight)
        alphaImg = None
    else:
        width, height = settings['dimensions']
        if settings['AA']:
            width *= 2
            height *= 2

            img = mh.renderToBuffer(width, height)
            alphaImg = mh.renderAlphaMask(width, height)
            img = imgop.addAlpha(img, imgop.getChannel(alphaImg, 0))

        if settings['AA']:
            img = img.resized(width/2, height/2, filter=image.FILTER_BILINEAR)
            img.data[:, :, :] = img.data[:, :, (2, 1, 0, 3)]

    if settings['lightmapSSS']:
        human.material = material_backup

    return img