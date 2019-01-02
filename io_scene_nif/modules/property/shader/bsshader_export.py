"""This script contains helper methods to custom shader."""

# ***** BEGIN LICENSE BLOCK *****
#
# Copyright © 2005-2018, NIF File Format Library and Tools contributors.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above
#      copyright notice, this list of conditions and the following
#      disclaimer in the documentation and/or other materials provided
#      with the distribution.
#
#    * Neither the name of the NIF File Format Library and Tools
#      project nor the names of its contributors may be used to endorse
#      or promote products derived from this software without specific
#      prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
#
# ***** END LICENSE BLOCK *****

from pyffi.formats.nif import NifFormat

from io_scene_nif.utility import nif_utils


class BSShaderProperty:

    @staticmethod
    def export_shader_flags(b_obj, shader):
        b_flag_list = b_obj.niftools_shader.bl_rna.properties.keys()
        if hasattr(shader, 'shader_flags'):
            for sf_flag in shader.shader_flags._names:
                if sf_flag in b_flag_list:
                    b_flag = b_obj.niftools_shader.get(sf_flag)
                    if b_flag:
                        sf_flag_index = shader.shader_flags._names.index(sf_flag)
                        shader.shader_flags._items[sf_flag_index]._value = 1

        if hasattr(shader, 'shader_flags_1'):
            for sf_flag in shader.shader_flags_1._names:
                if sf_flag in b_flag_list:
                    b_flag = b_obj.niftools_shader.get(sf_flag)
                    if b_flag:
                        sf_flag_index = shader.shader_flags_1._names.index(sf_flag)
                        shader.shader_flags_1._items[sf_flag_index]._value = 1

        if hasattr(shader, 'shader_flags_2'):
            for sf_flag in shader.shader_flags_2._names:
                if sf_flag in b_flag_list:
                    b_flag = b_obj.niftools_shader.get(sf_flag)
                    if b_flag:
                        sf_flag_index = shader.shader_flags_2._names.index(sf_flag)
                        shader.shader_flags_2._items[sf_flag_index]._value = 1

        return shader

    # TODO [property][shader]
    def export_bs_shader_property(self, b_obj=None, b_mat=None):
        """Export a Bethesda shader property block."""
        self.determine_texture_types(b_obj, b_mat)

        # create new block
        if b_obj.niftools_shader.bs_shadertype == 'BSShaderPPLightingProperty':
            bsshader = NifFormat.BSShaderPPLightingProperty()
            # set shader options
            # TODO [property][shader]
            b_s_type = NifFormat.BSShaderType._enumkeys.index(b_obj.niftools_shader.bsspplp_shaderobjtype)
            bsshader.shader_type = NifFormat.BSShaderType._enumvalues[b_s_type]

            # Shader Flags
            if hasattr(bsshader, 'shader_flags'):
                self.export_shader_flags(b_obj, bsshader)

        if b_obj.niftools_shader.bs_shadertype == 'BSLightingShaderProperty':
            bsshader = NifFormat.BSLightingShaderProperty()
            b_s_type = NifFormat.BSLightingShaderPropertyShaderType._enumkeys.index(
                b_obj.niftools_shader.bslsp_shaderobjtype)
            bsshader.shader_type = NifFormat.BSLightingShaderPropertyShaderType._enumvalues[b_s_type]

            # TODO [property][material]
            # UV Offset
            if hasattr(bsshader, 'uv_offset'):
                self.export_uv_offset(bsshader)

            # UV Scale
            if hasattr(bsshader, 'uv_scale'):
                self.export_uv_scale(bsshader)

            # Texture Clamping mode
            if not self.base_mtex.texture.image.use_clamp_x:
                wrap_s = 2
            else:
                wrap_s = 0
            if not self.base_mtex.texture.image.use_clamp_y:
                wrap_t = 1
            else:
                wrap_t = 0
            bsshader.texture_clamp_mode = (wrap_s + wrap_t)

            # Diffuse color
            bsshader.skin_tint_color.r = b_mat.diffuse_color.r
            bsshader.skin_tint_color.g = b_mat.diffuse_color.g
            bsshader.skin_tint_color.b = b_mat.diffuse_color.b
            # b_mat.diffuse_intensity = 1.0

            bsshader.lighting_effect_1 = b_mat.niftools.lightingeffect1
            bsshader.lighting_effect_2 = b_mat.niftools.lightingeffect2

            # Emissive
            bsshader.emissive_color.r = b_mat.niftools.emissive_color.r
            bsshader.emissive_color.g = b_mat.niftools.emissive_color.g
            bsshader.emissive_color.b = b_mat.niftools.emissive_color.b
            bsshader.emissive_multiple = b_mat.emit

            # gloss
            bsshader.glossiness = b_mat.specular_hardness

            # Specular color
            bsshader.specular_color.r = b_mat.specular_color.r
            bsshader.specular_color.g = b_mat.specular_color.g
            bsshader.specular_color.b = b_mat.specular_color.b
            bsshader.specular_strength = b_mat.specular_intensity

            # Alpha
            if b_mat.use_transparency:
                bsshader.alpha = (1 - b_mat.alpha)

            # Shader Flags
            if hasattr(bsshader, 'shader_flags_1'):
                self.export_shader_flags(b_obj, bsshader)

        if b_obj.niftools_shader.bs_shadertype == 'BSEffectShaderProperty':
            bsshader = NifFormat.BSEffectShaderProperty()

            # Alpha
            if b_mat.use_transparency:
                bsshader.alpha = (1 - b_mat.alpha)

            # clamp Mode
            bsshader.texture_clamp_mode = 65283

            # Emissive
            bsshader.emissive_color.r = b_mat.niftools.emissive_color.r
            bsshader.emissive_color.g = b_mat.niftools.emissive_color.g
            bsshader.emissive_color.b = b_mat.niftools.emissive_color.b
            bsshader.emissive_color.a = b_mat.niftools.emissive_alpha
            bsshader.emissive_multiple = b_mat.emit

            # Shader Flags
            if hasattr(bsshader, 'shader_flags_1'):
                self.export_shader_flags(b_obj, bsshader)

        if b_obj.niftools_shader.bs_shadertype == 'None':
            raise nif_utils.NifError("Export version expected shader. "
                                     "No shader applied to mesh '%s', these cannot be exported to NIF."
                                     " Set shader before exporting." % b_obj)
        # set textures
        texset = NifFormat.BSShaderTextureSet()
        bsshader.texture_set = texset
        if self.base_mtex:
            texset.textures[0] = self.texture_writer.export_texture_filename(self.base_mtex.texture)
        if self.normal_mtex:
            texset.textures[1] = self.texture_writer.export_texture_filename(self.normal_mtex.texture)
        if self.glow_mtex:
            texset.textures[2] = self.texture_writer.export_texture_filename(self.glow_mtex.texture)
        if self.detail_mtex:
            texset.textures[3] = self.texture_writer.export_texture_filename(self.detail_mtex.texture)

        if b_obj.niftools_shader.bs_shadertype == 'BSLightingShaderProperty':
            texset.num_textures = 9
            texset.textures.update_size()
            if self.detail_mtex:
                texset.textures[6] = self.texture_writer.export_texture_filename(self.detail_mtex.texture)
            if self.gloss_mtex:
                texset.textures[7] = self.texture_writer.export_texture_filename(self.gloss_mtex.texture)

        if b_obj.niftools_shader.bs_shadertype == 'BSEffectShaderProperty':
            bsshader.source_texture = self.texture_writer.export_texture_filename(self.base_mtex.texture)
            bsshader.greyscale_texture = self.texture_writer.export_texture_filename(self.glow_mtex.texture)

        return bsshader
