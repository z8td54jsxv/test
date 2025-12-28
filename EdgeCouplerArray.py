# N个Edge Coupler组成的阵列，间距127 um
import ipkiss3.all as i3
import si_fab.all as pdk

class edge_coupler_array(i3.Circuit):
    """N 个 Edge-(Grating) Coupler 阵列，间距 127 um"""

    edge_coupler = i3.ChildCellProperty(doc="edge coupler")
    pitch = i3.NumberProperty(default=127.0)
    n = i3.PositiveIntProperty(default=8)

    def _default_edge_coupler(self):
        # 👉 用 Grating Coupler 作为 Edge Coupler
        return pdk.GratingCoupler()

    def _default_insts(self):
        return {
            f"ec_{i}": self.edge_coupler
            for i in range(self.n)
        }

    def _default_specs(self):
        specs = []
        for i in range(self.n):
            y = i * self.pitch
            specs += [
                i3.Place(f"ec_{i}", (0, - y), angle=180)
            ]
        return specs


    def _default_exposed_ports(self):
        exposed_ports = {}

        for i in range(self.n):
            # 光纤侧：vertical_in 作为“芯片外部 IO”
            exposed_ports[f"ec_{i}:vertical_in"] = f"ec_in_{i}"

            # 波导侧：out 作为“连到片上波导”的口
            exposed_ports[f"ec_{i}:out"] = f"ec_wg_{i}"

        return exposed_ports

# N = 8  # 8个边缘耦合器
# output_spacing = 127  # 边缘耦合器之间的间距（单位：微米）
# x_pos = 0             # 边缘耦合器的x坐标（单位：微米）
# top_y = 175           # 边缘耦合器最顶部的y坐标（单位：微米）
#
# class Edge_coupler_array(i3.Circuit):
#     ec = i3.ChildCellProperty(doc="edge_coupler")
#
#     def _default_ec(self):
#         return pdk.SiNInvertedTaper()
#
#     def _default_insts(self):
#         insts = {}
#         # 创建边缘耦合器阵列
#         for i in range(N):
#             insts[f"ec_out_{i}"] = self.ec
#         return insts
#
#     def _default_specs(self):
#         specs = []
#         # 创建一个空列表来存储连接规范
#         # 放置边缘耦合器，垂直排列
#
#         for i in range(N):
#             # 从顶部开始向下放置：ec_out_0在最上面，ec_out_7在最下面
#             y_pos = top_y - i * output_spacing
#             specs.append(i3.Place(f"ec_out_{i}", (x_pos, y_pos), angle=0))
#         return specs
#
#     def _default_exposed_ports(self):
#         # exposed_ports指定哪些内部端口需要暴露为阵列的外部端口
#         exposed_ports = {}
#
#         for i in range(N):
#             # 添加输入端口
#             exposed_ports[f"ec_out_{i}:in"] = f"in{i}"
#             # 添加输出端口
#             exposed_ports[f"ec_out_{i}:out"] = f"out{i}"
#


if __name__ == "__main__":
    test = edge_coupler_array()
    test.Layout().visualize()