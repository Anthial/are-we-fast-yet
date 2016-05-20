# Adapted based on SOM benchmark.
# Copyright 2011 Google Inc.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#         limitations under the License.
require "./benchmark"
require "./som"

class Havlak < Benchmark
  def inner_benchmark_loop(inner_iterations)
    verify_result(LoopTesterApp.new.main(
        inner_iterations, 50, 10, 10, 5), inner_iterations)
  end

  def verify_result(result, inner_iterations)
    if inner_iterations == 15000; return result[0] == 46602 && result[1] == 5213 end
    if inner_iterations ==  1500; return result[0] ==  6102 && result[1] == 5213 end
    if inner_iterations ==   150; return result[0] ==  2052 && result[1] == 5213 end
    if inner_iterations ==    15; return result[0] ==  1647 && result[1] == 5213 end
    if inner_iterations ==     1; return result[0] ==  1605 && result[1] == 5213 end

    puts("No verification result for " + inner_iterations.to_s + " found")
    puts("Result is: " + r[0].to_s + ", " + r[1].to_s)
    false
  end
end

class BasicBlock
  getter :in_edges, :out_edges

  def initialize(name)
    @name = name
    @in_edges  = Vector.new(2)
    @out_edges = Vector.new(2)
  end

  def num_pred
    @in_edges.size
  end

  def add_out_edge(to)
    @out_edges.append(to)
  end

  def add_in_edge(from)
    @in_edges.append(from)
  end

  def custom_hash
    @name
  end
end

class BasicBlockEdge
  def initialize(cfg, from_name, to_name)
    @from = cfg.create_node(from_name)
    @to   = cfg.create_node(to_name)

    @from.add_out_edge(@to)
    @to.add_in_edge(@from)

    cfg.add_edge(self)
  end
end

class ControlFlowGraph
  def initialize
    @start_node = nil
    @basic_block_map = Vector.new
    @edge_list = Vector.new
  end

  def create_node(name)
    if @basic_block_map.at(name)
      node = @basic_block_map.at(name)
    else
      node = BasicBlock.new(name)
      @basic_block_map.at_put(name, node)
    end

    if num_nodes == 1
      @start_node = node
    end
    node
  end

  def add_edge(edge)
    @edge_list.append(edge)
  end

  def num_nodes
    @basic_block_map.size
  end

  def get_start_basic_block
    @start_node
  end

  def get_basic_blocks
    @basic_block_map
  end
end

def max(a, b)
  a < b ? b : a
end

class LoopStructureGraph
  def initialize
    @loop_counter = 0
    @loops = Vector.new
    @root = SimpleLoop.new(nil, true)
    @root.set_nesting_level(0)
    @root.counter = @loop_counter
    @loop_counter += 1
    @loops.append(@root)
  end

  def create_new_loop(bb, is_reducible)
    loop = SimpleLoop.new(bb, is_reducible)
    loop.counter = @loop_counter
    @loop_counter += 1
    @loops.append(loop)
    loop
  end

  def calculate_nesting_level
    @loops.each { |liter|
      unless liter.is_root
        if liter.parent == nil
          liter.set_parent(@root)
        end
      end
    }

    calculate_nesting_level_rec(@root, 0)
  end

  def calculate_nesting_level_rec(loop, depth)
    loop.depth_level = depth
    loop.children.each { |liter|
      calculate_nesting_level_rec(liter, depth + 1)
      loop.set_nesting_level(max(loop.nesting_level, 1 + liter.nesting_level))
    }
  end

  def num_loops
    @loops.size
  end
end

class SimpleLoop
  getter :children, :parent, :nesting_level, :is_root
  setter :counter, :depth_level

  def initialize(bb, is_reducible)
    @is_reducible = is_reducible
    @parent = nil
    @is_root = false
    @nesting_level = 0
    @depth_level   = 0
    @counter       = 0
    @basic_blocks  = IdentitySet.new
    @children      = IdentitySet.new

    if bb
      @basic_blocks.add(bb)
    end

    @header = bb
  end

  def add_node(bb)
    @basic_blocks.add(bb)
  end

  def add_child_loop(loop)
    @children.add(loop)
  end

  def set_parent(parent)
    @parent = parent
    @parent.add_child_loop(self)
  end

  def set_is_root
    @is_root = true
  end

  def set_nesting_level(level)
    @nesting_level = level
    if level == 0
      set_is_root
    end
  end
end

class UnionFindNode
  getter :bb, :dfs_number, :parent
  property :loop

  def initialize
    @parent = nil
    @bb     = nil
    @dfs_number = 0
    @loop   = nil
  end

  def init_node(bb, dfs_number)
    @parent = self
    @bb     = bb
    @dfs_number = dfs_number
    @loop   = nil
  end

  def find_set
    node_list = Vector.new

    node = self
    until node.equal? node.parent
      unless node.parent.equal? node.parent.parent
        node_list.append(node)
      end
      node = node.parent
    end

    node_list.each { |iter| iter.union(@parent) }
    node
  end

  def union(basic_block)
    @parent = basic_block
  end
end

class LoopTesterApp
  def initialize
    @cfg = ControlFlowGraph.new
    @lsg = LoopStructureGraph.new
    @cfg.create_node(0)
  end

  def build_diamond(start)
    bb0 = start
    BasicBlockEdge.new(@cfg, bb0, bb0 + 1)
    BasicBlockEdge.new(@cfg, bb0, bb0 + 2)
    BasicBlockEdge.new(@cfg, bb0 + 1, bb0 + 3)
    BasicBlockEdge.new(@cfg, bb0 + 2, bb0 + 3)
    bb0 + 3
  end

  def build_connect(start, end_)
    BasicBlockEdge.new(@cfg, start, end_)
  end

  def build_straight(start, n)
    (0...n).each { |i|
      build_connect(start + i, start + i + 1)
    }
    start + n
  end

  def build_base_loop(from)
    header   = build_straight(from, 1)
    diamond1 = build_diamond(header)
    d11      = build_straight(diamond1, 1)
    diamond2 = build_diamond(d11)
    footer   = build_straight(diamond2, 1)
    build_connect(diamond2, d11)
    build_connect(diamond1, header)

    build_connect(footer, from)
    footer = build_straight(footer, 1)
    footer
  end

  def main(num_dummy_loops, find_loop_iterations, par_loops, ppar_loops, pppar_loops)
    construct_simple_cfg
    add_dummy_loops(num_dummy_loops)
    construct_cfg(par_loops, ppar_loops, pppar_loops)

    find_loops(@lsg)

    find_loop_iterations.times {
      find_loops(LoopStructureGraph.new)
    }

    @lsg.calculate_nesting_level
    [@lsg.num_loops, @cfg.num_nodes]
  end

  def construct_cfg(par_loops, ppar_loops, pppar_loops)
    n = 2

    par_loops.times {
      @cfg.create_node(n + 1)
      build_connect(2, n + 1)
      n += 1

      ppar_loops.times {
        top = n
        n = build_straight(n, 1)
        pppar_loops.times { n = build_base_loop(n) }
        bottom = build_straight(n, 1)
        build_connect(n, top)
        n = bottom
      }
      build_connect(n, 1)
    }
  end

  def add_dummy_loops(num_dummy_loops)
    num_dummy_loops.times { find_loops(@lsg) }
  end

  def find_loops(loop_structure)
    finder = HavlakLoopFinder.new(@cfg, loop_structure)
    finder.find_loops
  end

  def construct_simple_cfg
    @cfg.create_node(0)
    build_base_loop(0)
    @cfg.create_node(1)
    BasicBlockEdge.new(@cfg, 0, 2)
  end
end

UNVISITED = 2147483647
MAXNONBACKPREDS = 32 * 1024

class HavlakLoopFinder

  def initialize(cfg, lsg)
    @cfg = cfg
    @lsg = lsg
    @non_back_preds = Vector.new
    @back_preds     = Vector.new
    @number         = IdentityDictionary.new
    @max_size = 0
    @header = nil
    @type   = nil
    @last   = nil
    @nodes  = nil
  end

  def is_ancestor(w, v)
    w <= v && v <= @last[w]
  end

  def do_dfs(current_node, current)
    @nodes[current].init_node(current_node, current)
    @number.at_put(current_node, current)

    last_id = current
    outer_blocks = current_node.out_edges

    outer_blocks.each { |target|
      if @number.at(target) == UNVISITED
        last_id = do_dfs(target, last_id + 1)
      end
    }

    @last[current] = last_id
    last_id
  end

  def init_all_nodes
    @cfg.get_basic_blocks.each { |bbIter|
      @number.at_put(bbIter, UNVISITED)
    }

    do_dfs(@cfg.get_start_basic_block, 0)
  end

  def identify_edges(size)
    (0...size).each { |w|
      @header[w] = 0
      @type[w] = :BB_NONHEADER

      node_w = @nodes[w].bb
      if node_w == nil
        @type[w] = :BB_DEAD
      else
        process_edges(node_w, w)
      end
    }
  end

  def process_edges(node_w, w)
    if node_w.num_pred > 0
      node_w.in_edges.each { |node_v|
        v = @number.at(node_v)
        unless v == UNVISITED
          if is_ancestor(w, v)
            @back_preds.at(w).append(v)
          else
            @non_back_preds.at(w).add(v)
          end
        end
      }
    end
  end

  def find_loops
    if @cfg.get_start_basic_block == nil; return end

    size = @cfg.num_nodes
    @non_back_preds.remove_all
    @back_preds.remove_all
    @number.remove_all

    if size > @max_size
      @header   = Array.new(size)
      @type     = Array.new(size)
      @last     = Array.new(size)
      @nodes    = Array.new(size)
      @max_size = size
    end

    (0...size).each { |i|
      @non_back_preds.append(Set.new)
      @back_preds.append(Vector.new)
      @nodes[i] = UnionFindNode.new
    }

    init_all_nodes
    identify_edges(size)

    @header[0] = 0

    (size - 1).downto(0) { |w|
      node_pool = Vector.new
      node_w = @nodes[w].bb
      if node_w
        step_d(w, node_pool)

        work_list = Vector.new
        node_pool.each { |niter| work_list.append(niter) }

        if node_pool.size != 0
          @type[w] = :BB_REDUCIBLE
        end

        until work_list.empty?
          x = work_list.remove_first
          non_back_size = @non_back_preds.at(x.dfs_number).size
          if non_back_size > MAXNONBACKPREDS; return end
          step_e_process_non_back_preds(w, node_pool, work_list, x)
        end
      end

      if node_pool.size > 0 || @type[w] == :BB_SELF
        loop = @lsg.create_new_loop(node_w, @type[w] != :BB_IRREDUCIBLE)
        set_loop_attributes(w, node_pool, loop)
      end
    }
  end

  def step_e_process_non_back_preds(w, node_pool, work_list, x)
    @non_back_preds.at(x.dfs_number).each { |iter|
      y = @nodes[iter]
      ydash = y.find_set

      if !is_ancestor(w, ydash.dfs_number)
        @type[w] = :BB_IRREDUCIBLE
        @non_back_preds.at(w).add(ydash.dfs_number)
      else
        if ydash.dfs_number != w
          work_list.append(ydash)
          node_pool.append(ydash)
        end
      end
    }
  end

  def set_loop_attributes(w, node_pool, loop)
    @nodes[w].loop = loop
    node_pool.each { |node|
      @header[node.dfs_number] = w
      node.union(@nodes[w])

      if node.loop
        node.loop.set_parent(loop)
      else
        loop.add_node(node.bb)
      end
    }
  end

  def step_d(w, node_pool)
    @back_preds.at(w).each { |v|
      if v != w
        node_pool.append(@nodes[v].find_set)
      else
        @type[w] = :BB_SELF
      end
    }
  end
end
