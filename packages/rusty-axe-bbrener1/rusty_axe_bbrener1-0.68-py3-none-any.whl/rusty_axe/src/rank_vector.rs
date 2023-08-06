use crate::io::DispersionMode;
use crate::utils::{slow_mad};
use crate::argminmax::*;
use ndarray::prelude::*;
use smallvec::SmallVec;
use std::borrow::{Borrow, BorrowMut};
use std::clone::Clone;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::collections::HashSet;
use std::f64;
use std::fmt::Debug;
use std::ops::Index;
use std::ops::IndexMut;

#[derive(Clone, Serialize, Deserialize)]
pub struct RankVector<T> {
    pub rank_order: Option<Vec<usize>>,
    zones: [usize; 4],
    sums: [f64; 2],
    squared_sums: [f64; 2],
    offset: usize,
    median: (usize, usize),
    left: usize,
    right: usize,
    nodes: T,
}

#[derive(Clone, Copy, Debug, Serialize, Deserialize)]
pub struct Node {
    data: f64,
    index: usize,
    rank: usize,
    previous: usize,
    next: usize,
    zone: usize,
}

impl Node {
    pub fn blank() -> Node {
        Node {
            data: f64::NAN,
            index: 0,
            rank: 0,
            previous: 0,
            next: 0,
            zone: 0,
        }
    }
}

impl<
        T: Borrow<[Node]>
            + BorrowMut<[Node]>
            + Index<usize, Output = Node>
            + IndexMut<usize, Output = Node>
            + Clone
            + Debug,
    > RankVector<T>
{
    pub fn empty() -> RankVector<Vec<Node>> {
        RankVector::<Vec<Node>>::link(&vec![])
    }

    pub fn link_array(in_arr: ArrayView1<f64>) -> RankVector<Vec<Node>> {
        let argsorted: Vec<(usize, &f64)> = in_arr.argsort();
        RankVector::<Vec<Node>>::link_sorted(argsorted)
    }

    pub fn link(in_vec: &[f64]) -> RankVector<Vec<Node>> {
        let argsorted: Vec<(usize, &f64)> = in_vec.argsort();
        RankVector::<Vec<Node>>::link_sorted(argsorted)
    }

    pub fn link_sorted(argsorted: Vec<(usize, &f64)>) -> RankVector<Vec<Node>> {
        // This method accepts argsorted vectors of f64s only. It does not check integrity!
        // Use at own risk.

        let mut vector: Vec<Node> = vec![Node::blank(); argsorted.len() + 2];

        let left = vector.len() - 2;
        let right = vector.len() - 1;

        vector[left] = Node {
            data: 0.,
            index: left,
            rank: 0,
            previous: left,
            next: right,
            zone: 0,
        };

        vector[right] = Node {
            data: 0.,
            index: right,
            rank: 0,
            previous: left,
            next: right,
            zone: 0,
        };

        let mut zones = [0; 4];
        let mut sums = [0.; 2];
        let mut squared_sums = [0.; 2];

        let mut previous = left;
        let tail_node_index = right;
        let mut rank_order = Vec::with_capacity(argsorted.len());

        for (ranking, (index, data)) in argsorted.into_iter().enumerate() {
            let node = &mut vector[index];

            node.data = *data;
            node.index = index;
            node.previous = previous;
            node.next = tail_node_index;
            node.zone = 2;
            node.rank = ranking;

            vector[previous].next = index;
            previous = index;
            rank_order.push(index);

            zones[2] += 1;
            sums[1] += data;
            squared_sums[1] += data.powi(2);
        }

        vector[right].previous = previous;

        let median = (vector.len() - 2, vector.len() - 2);

        let left = *rank_order.get(0).unwrap_or(&0);
        let right = *rank_order.last().unwrap_or(&0);

        let mut prototype = RankVector::<Vec<Node>> {
            nodes: vector,
            rank_order: Some(rank_order),
            zones: zones,
            sums: sums,
            squared_sums: squared_sums,
            offset: 2,
            median: median,
            left: left,
            right: right,
        };

        prototype.establish_median();

        prototype.establish_zones();

        prototype
    }

    #[inline]
    pub fn g_left(&self, index: usize) -> usize {
        self.nodes[index].previous
    }

    #[inline]
    pub fn g_right(&self, index: usize) -> usize {
        self.nodes[index].next
    }

    #[inline]
    pub fn pop(&mut self, target: usize) -> f64 {
        let target_zone = self.nodes[target].zone;

        if target_zone != 0 {

            self.unlink(target);

            self.zones[target_zone] -= 1;
            self.zones[0] += 1;

            if self.nodes[target].rank < self.nodes[self.median.1].rank {
                self.sums[0] -= self.nodes[target].data;
                self.squared_sums[0] -= self.nodes[target].data.powi(2);
            }
            if self.nodes[target].rank > self.nodes[self.median.0].rank {
                self.sums[1] -= self.nodes[target].data;
                self.squared_sums[1] -= self.nodes[target].data.powi(2);
            }

            self.nodes[target].zone = 0;

            self.check_boundaries(target);

            self.balance_zones();

            let (old_median, new_median) = self.recenter_median(target);

            self.shift_zones(old_median, new_median);
        }

        self.nodes[target].data
    }

    #[inline]
    fn mpop(&mut self, target: usize) -> (f64, f64) {
        let target_zone = self.nodes[target].zone;
        if target_zone != 0 {

            self.unlink(target);
            self.zones[target_zone] -= 1;
            self.zones[0] += 1;

            if self.nodes[target].rank < self.nodes[self.median.1].rank {
                self.sums[0] -= self.nodes[target].data;
                self.squared_sums[0] -= self.nodes[target].data.powi(2);
            }
            if self.nodes[target].rank > self.nodes[self.median.0].rank {
                self.sums[1] -= self.nodes[target].data;
                self.squared_sums[1] -= self.nodes[target].data.powi(2);
            }

            let (_old_median, new_median) = self.recenter_median(target);

            (new_median, self.nodes[target].data)
        } else {
            (self.median(), self.nodes[target].data)
        }
    }

    #[inline]
    fn unlink(&mut self, target: usize) {
        let left = self.nodes[target].previous;
        let right = self.nodes[target].next;

        self.nodes[left].next = self.nodes[target].next;
        self.nodes[right].previous = self.nodes[target].previous;
    }

    #[inline]
    fn check_boundaries(&mut self, target: usize) {
        match target {
            left if left == self.left => {
                self.left = self.nodes[target].next;
            }
            right if right == self.right => {
                self.right = self.nodes[target].previous;
            }
            _ => {}
        }
    }

    //

    #[inline]
    pub fn establish_median(&mut self) {
        let order = self.left_to_right();

        // eprintln!("Establishing median: order:{:?}",order);

        match order.len() % 2 {
            0 => {
                if order.len() == 0 {
                    self.median = (0, 1)
                } else {
                    let m = order.len() / 2;
                    self.median = (order[m - 1], order[m]);
                    let l_sum = order[..m].iter().map(|&i| self.nodes[i].data).sum::<f64>();
                    let r_sum = order[m..].iter().map(|&i| self.nodes[i].data).sum::<f64>();
                    let l_squared_sum = order[..m]
                        .iter()
                        .map(|&i| self.nodes[i].data.powi(2))
                        .sum::<f64>();
                    let r_squared_sum = order[m..]
                        .iter()
                        .map(|&i| self.nodes[i].data.powi(2))
                        .sum::<f64>();
                    self.sums = [l_sum, r_sum];
                    self.squared_sums = [l_squared_sum, r_squared_sum];
                    // eprintln!("Establishing median:{:?},{:?}",self.median,self.sums);
                }
            }
            1 => {
                let m = order.len() / 2;
                self.median = (order[m], order[m]);
                let l_sum = order[..m].iter().map(|&i| self.nodes[i].data).sum::<f64>();
                let r_sum = order[(m + 1)..]
                    .iter()
                    .map(|&i| self.nodes[i].data)
                    .sum::<f64>();
                let l_squared_sum = order[..m]
                    .iter()
                    .map(|&i| self.nodes[i].data.powi(2))
                    .sum::<f64>();
                let r_squared_sum = order[(m + 1)..]
                    .iter()
                    .map(|&i| self.nodes[i].data.powi(2))
                    .sum::<f64>();
                self.sums = [l_sum, r_sum];
                self.squared_sums = [l_squared_sum, r_squared_sum];
                // eprintln!("Establishing median:{:?},{:?}",self.median,self.sums);
            }
            _ => unreachable!(),
        }
    }

    #[inline]
    pub fn establish_zones(&mut self) {
        for _ in 0..(((self.len()) / 2).max(1) - (1 - self.len() % 2)) {
            self.contract_1();
        }
    }

    #[inline]
    pub fn len(&self) -> usize {
        self.zones[1] + self.zones[2] + self.zones[3]
    }

    #[inline]
    pub fn raw_len(&self) -> usize {
        self.zones[0] + self.zones[1] + self.zones[2] + self.zones[3]
    }

    #[inline]
    pub fn contract_left(&mut self) {
        self.zones[1] += 1;
        self.zones[2] -= 1;

        self.nodes[self.left].zone = 1;
        self.left = self.nodes[self.left].next;
    }

    #[inline]
    pub fn contract_right(&mut self) {
        self.zones[3] += 1;
        self.zones[2] -= 1;

        self.nodes[self.right].zone = 3;
        self.right = self.nodes[self.right].previous;
    }

    #[inline]
    pub fn expand_left(&mut self) {
        self.zones[1] -= 1;
        self.zones[2] += 1;

        self.left = self.nodes[self.left].previous;
        self.nodes[self.left].zone = 2;
    }

    #[inline]
    pub fn expand_right(&mut self) {
        self.zones[3] -= 1;
        self.zones[2] += 1;

        self.right = self.nodes[self.right].next;
        self.nodes[self.right].zone = 2;
    }

    #[inline]
    pub fn move_left(&mut self) {
        self.expand_left();
        self.contract_right();
    }

    #[inline]
    pub fn move_right(&mut self) {
        self.expand_right();
        self.contract_left();
    }

    #[inline]
    pub fn expand_1(&mut self) {
        let median = self.median();

        if self.zones[1] > 0 && self.zones[3] > 0 {
            let left = self.nodes[self.nodes[self.left].previous].data;
            let right = self.nodes[self.nodes[self.right].next].data;

            if (right - median).abs() > (median - left).abs() {
                self.expand_left();
            } else {
                self.expand_right();
            }
        } else {
            if self.zones[3] != 0 {
                self.expand_right();
            } else if self.zones[1] != 0 {
                self.expand_left();
            } else {
                panic!("Tried to expand into empty boundary zones!")
            }
        }
    }

    #[inline]
    pub fn contract_1(&mut self) {
        let median = self.median();

        let left = self.nodes[self.left].data;
        let right = self.nodes[self.right].data;

        if (right - median).abs() > (left - median).abs() {
            self.contract_right();
        } else {
            self.contract_left();
        }
    }

    #[inline]
    pub fn balance_zones(&mut self) {
        if self.len() > 0 {
            match self.len() % 2 {
                1 => match self.zones[2].cmp(&(self.zones[1] + self.zones[3] + 1)) {
                    Ordering::Greater => self.contract_1(),
                    Ordering::Less => self.expand_1(),
                    Ordering::Equal => {}
                },
                0 => match self.zones[2].cmp(&(self.zones[1] + self.zones[3] + 2)) {
                    Ordering::Greater => self.contract_1(),
                    Ordering::Less => self.expand_1(),
                    Ordering::Equal => {}
                },
                _ => unreachable!(),
            }
        }
    }

    #[inline]
    pub fn median(&self) -> f64 {
        (self.nodes[self.median.0].data + self.nodes[self.median.1].data) / 2.
    }

    pub fn sum(&self) -> f64 {
        if self.len() % 2 == 0 {
            self.sums[0] + self.sums[1]
        } else {
            self.sums[0] + self.sums[1] + self.median()
        }
    }

    pub fn sum_of_squares(&self) -> f64 {
        if self.len() % 2 == 0 {
            self.squared_sums[0] + self.squared_sums[1]
        } else {
            self.squared_sums[0] + self.squared_sums[1] + self.median().powi(2)
        }
    }

    #[inline]
    pub fn shift_median_left(&mut self) {
        match self.median.0 == self.median.1 {
            false => {
                self.sums[0] -= self.nodes[self.median.0].data;
                self.squared_sums[0] -= self.nodes[self.median.0].data.powi(2);
                self.median = (
                    self.nodes[self.median.1].previous,
                    self.nodes[self.median.1].previous,
                )
            }
            true => {
                self.sums[1] += self.nodes[self.median.1].data;
                self.squared_sums[1] += self.nodes[self.median.1].data.powi(2);
                self.median = (self.nodes[self.median.1].previous, self.median.1)
            }
        }
    }

    #[inline]
    pub fn shift_median_right(&mut self) {
        match self.median.0 == self.median.1 {
            false => {
                self.sums[1] -= self.nodes[self.median.1].data;
                self.squared_sums[1] -= self.nodes[self.median.1].data.powi(2);
                self.median = (
                    self.nodes[self.median.0].next,
                    self.nodes[self.median.0].next,
                )
            }
            true => {
                self.sums[0] += self.nodes[self.median.0].data;
                self.squared_sums[0] += self.nodes[self.median.0].data.powi(2);
                self.median = (self.median.0, self.nodes[self.median.0].next)
            }
        }
    }

    #[inline]
    pub fn recenter_median(&mut self, target: usize) -> (f64, f64) {
        let old_median = self.median();

        let target_rank = self.nodes[target].rank;
        let left_rank = self.nodes[self.median.0].rank;
        let right_rank = self.nodes[self.median.1].rank;

        if target_rank > left_rank {
            self.shift_median_left();
        } else if target_rank < right_rank {
            self.shift_median_right();
        } else {
            self.median.0 = self.nodes[target].previous;
            self.median.1 = self.nodes[target].next;
        }

        let new_median = self.median();

        (old_median, new_median)
    }

    #[inline]
    pub fn shift_zones(&mut self, old_median: f64, new_median: f64) {
        let change = new_median - old_median;

        if change > 0. {
            for _ in 0..self.zones[3] {
                let left = self.nodes[self.left].data;
                let right = self.nodes[self.nodes[self.right].next].data;


                if (right - new_median).abs() > (left - new_median).abs() {
                    break;
                }

                self.move_right()
            }
        }
        if change < 0. {
            for _ in 0..self.zones[1] {
                let left = self.nodes[self.nodes[self.left].previous].data;
                let right = self.nodes[self.right].data;

                if (left - new_median).abs() > (right - new_median).abs() {
                    break;
                }

                self.move_left()
            }
        }
    }

    #[inline]
    pub fn mad(&self) -> f64 {
        if self.len() < 2 {
            return 0.;
        }

        let left_i = self.left;
        let right_i = self.right;

        let inner_left_i = self.nodes[left_i].next;
        let inner_right_i = self.nodes[right_i].previous;

        let left = self.nodes[left_i].data;
        let right = self.nodes[right_i].data;
        let inner_left = self.nodes[inner_left_i].data;
        let inner_right = self.nodes[inner_right_i].data;

        let median = self.median();

        let mut distance_to_median = [
            (left - median).abs(),
            (inner_left - median).abs(),
            (inner_right - median).abs(),
            (right - median).abs(),
        ];

        distance_to_median.sort_unstable_by(|a, b| a.partial_cmp(&b).unwrap_or(Ordering::Greater));
        distance_to_median.reverse();

        if self.len() % 2 == 1 {
            return distance_to_median[0];
        } else {
            return (distance_to_median[0] + distance_to_median[1]) / 2.;
        }
    }

    #[inline]
    pub fn entropy(&self) -> f64 {
        if self.len() < 2 {
            return 0.;
        }

        let left = self.zones[1];
        let center = self.zones[2];
        let right = self.zones[3];
        let total = (left + right + center) as f64;

        let p_left = left as f64 / total;
        let p_center = center as f64 / total;
        let p_right = right as f64 / total;

        let mut left_entropy = 0.;
        let mut center_entropy = 0.;
        let mut right_entropy = 0.;

        if left > 0 {
            left_entropy = p_left.log2() * p_left;
        }
        if center > 0 {
            center_entropy = p_center.log2() * p_center;
        }
        if right > 0 {
            right_entropy = p_right.log2() * p_right;
        }

        return (left_entropy + center_entropy + right_entropy) * total;
    }

    #[inline]
    pub fn mean(&self) -> f64 {
        let sum: f64 = self.ordered_values().iter().sum();
        sum / self.len() as f64
    }

    #[inline]
    pub fn var(&self) -> f64 {
        let len = self.len() as f64;
        let mean = self.sum() / len;
        (self.sum_of_squares() / len) - mean.powi(2)


    }

    #[inline]
    pub fn sse(&self) -> f64 {
        let values = self.ordered_values();
        let len = self.len() as f64;
        let sum: f64 = values.iter().sum();
        let mean = sum / len;
        let deviation_sum: f64 = values.iter().map(|x| (x - mean).powi(2)).sum();
        deviation_sum
    }

    #[inline]
    pub fn ssme(&self) -> f64 {
        let sum = self.sum();
        let sum_of_squares = self.sum_of_squares();
        let median = self.median();
        let len = self.len() as f64;
        (median.powi(2) * len) - (2. * (median * sum)) + sum_of_squares
    }

    #[inline]
    pub fn sme(&self) -> f64 {
        let sig = self.median() * (self.len() / 2) as f64;
        let left = sig - self.sums[0];
        let right = self.sums[1] - sig;

        left + right
    }

    pub fn match_pop(&mut self, index: usize, mode: DispersionMode) -> f64 {
        match mode {
            DispersionMode::Variance
            | DispersionMode::MAD
            | DispersionMode::SSE
            | DispersionMode::Entropy => self.pop(index),
            DispersionMode::SSME | DispersionMode::SME => self.mpop(index).1,
            DispersionMode::Mixed => {
                panic!("Mixed mode not a valid dispersion for individual trees!")
            }
        }
    }

    #[inline]
    pub fn dispersion(&self, mode: DispersionMode) -> f64 {
        match mode {
            DispersionMode::Variance => self.var(),
            DispersionMode::SSE => self.sse(),
            DispersionMode::MAD => self.mad(),
            DispersionMode::SSME => self.ssme(),
            DispersionMode::SME => self.sme(),
            DispersionMode::Entropy => self.entropy(),
            DispersionMode::Mixed => {
                panic!("Mixed mode not a valid dispersion for individual trees!")
            }
        }
    }

    #[inline]
    pub fn l2(&self) -> f64 {
        let values = self.ordered_values();
        let median = self.median();
        values.iter().map(|x| (x - median).powi(2)).sum()
    }

    #[inline]
    pub fn left_to_right(&self) -> Vec<usize> {
        GRVCrawler::new(self, self.nodes[self.raw_len()].next)
            .take(self.len())
            .collect()
    }

    #[inline]
    pub fn ordered_values(&self) -> Vec<f64> {
        self.left_to_right()
            .iter()
            .map(|x| self.nodes[*x].data)
            .collect()
    }

    #[inline]
    pub fn full_values<'a>(&'a self) -> impl Iterator<Item = &'a f64> + 'a {
        (0..self.raw_len()).map(move |x| &self.nodes[x].data)
    }

    #[inline]
    pub fn full_values_with_state<'a>(&'a self) -> impl Iterator<Item = (bool, &'a f64)> + 'a {
        (0..self.raw_len()).map(move |x| (self.nodes[x].zone != 0, &self.nodes[x].data))
    }

    pub fn ordered_meds_mads(&mut self, draw_order: &[usize]) -> Vec<(f64, f64)> {
        let mut meds_mads = Vec::with_capacity(draw_order.len());
        meds_mads.push((self.median(), self.mad()));
        for draw in draw_order {
            self.pop(*draw);
            meds_mads.push((self.median(), self.mad()))
        }

        meds_mads
    }

    pub fn ordered_entropy(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut entropy = Vec::with_capacity(draw_order.len());
        entropy.push(self.entropy());
        for draw in draw_order {
            self.pop(*draw);
            entropy.push(self.entropy());
        }

        entropy
    }

    pub fn ordered_mad_gains(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let start_mad = self.mad();

        let mut mad_gains = Vec::with_capacity(draw_order.len());

        mad_gains.push(0.);
        for draw in draw_order {
            self.pop(*draw);
            mad_gains.push((start_mad - self.mad()).max(0.));
        }

        mad_gains
    }

    pub fn ordered_variance(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut variances = Vec::with_capacity(draw_order.len());

        let mut running_mean = 0.;
        let mut running_square_sum = 0.;

        for (i, draw) in draw_order.iter().rev().enumerate() {
            if self.nodes[*draw].zone != 0 {
                let target = self.nodes[*draw].data;
                let new_running_mean = running_mean + ((target - running_mean) / (i as f64 + 1.));
                let new_running_square_sum =
                    running_square_sum + (target - running_mean) * (target - new_running_mean);
                running_mean = new_running_mean;
                running_square_sum = new_running_square_sum;

                variances.push(running_square_sum / (i as f64 + 1.));
            } else {
                continue;
            }
        }

        variances.into_iter().rev().collect()
    }

    pub fn ordered_sse(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut sse = Vec::with_capacity(draw_order.len());

        let mut running_mean = 0.;
        let mut running_square_sum = 0.;

        for (i, draw) in draw_order.iter().rev().enumerate() {
            if self.nodes[*draw].zone != 0 {
                let target = self.nodes[*draw].data;
                let new_running_mean = running_mean + ((target - running_mean) / (i as f64 + 1.));
                let new_running_square_sum =
                    running_square_sum + (target - running_mean) * (target - new_running_mean);
                running_mean = new_running_mean;
                running_square_sum = new_running_square_sum;

                sse.push(running_square_sum - (running_mean * i as f64));
            } else {
                continue;
            }
        }

        sse.into_iter().rev().collect()
    }

    pub fn ordered_ssme(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut ssmes = Vec::with_capacity(draw_order.len());

        for draw in draw_order {
            ssmes.push(self.ssme());
            self.pop(*draw);
        }

        ssmes

    }

    pub fn ordered_sme(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut smes = Vec::with_capacity(draw_order.len());

        for draw in draw_order {
            smes.push(self.sme());
            self.pop(*draw);
        }

        smes

    }

    pub fn ordered_mads(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut mads = Vec::with_capacity(draw_order.len());
        mads.push(self.mad());
        for draw in draw_order {
            self.pop(*draw);
            mads.push(self.mad());
        }

        mads
    }

    pub fn ordered_covs(&mut self, draw_order: &[usize]) -> Vec<f64> {
        let mut covs = Vec::with_capacity(draw_order.len());

        covs.push(self.mad() / self.median());

        for draw in draw_order {
            self.pop(*draw);
            let cov = (self.mad() / self.median()).abs();
            covs.push(cov);
        }

        for element in covs.iter_mut() {
            if !element.is_normal() {
                *element = 0.;
            }
        }

        covs
    }

    pub fn ordered_dispersion(&mut self, draw_order: &[usize], mode: DispersionMode) -> Vec<f64> {
        match mode {
            DispersionMode::Variance => self.ordered_variance(&draw_order),
            DispersionMode::SSE => self.ordered_sse(&draw_order),
            DispersionMode::MAD => self.ordered_mads(&draw_order),
            DispersionMode::SSME => self.ordered_ssme(&draw_order),
            DispersionMode::SME => self.ordered_sme(&draw_order),
            DispersionMode::Entropy => self.ordered_entropy(&draw_order),
            DispersionMode::Mixed => {
                panic!("Mixed mode not a valid split setting for individual trees!")
            }
        }
    }

    #[inline]
    pub fn draw_order(&self) -> Vec<usize> {
        self.left_to_right()
    }

    #[inline]
    pub fn split_mask(&self, split: f64) -> Vec<bool> {
        let mut mask = vec![true; self.raw_len()];

        for (i, (d, v)) in self.full_values_with_state().enumerate() {
            if v <= &split && d {
                mask[i] = false;
            }
        }

        return mask;
    }


    pub fn ordered_cov_gains(
        &mut self,
        draw_order: &Vec<usize>,
        drop_set: &HashSet<usize>,
    ) -> Vec<f64> {
        for dropped_sample in drop_set {
            self.pop(*dropped_sample);
        }

        let mut cov_gains = Vec::with_capacity(draw_order.len());

        let mut start_cov = self.mad() / self.median();

        if !start_cov.is_normal() {
            start_cov = 0.;
        }

        cov_gains.push(0.);

        for draw in draw_order {
            let mut cov = self.mad() / self.median();

            if !cov.is_normal() {
                cov = 0.;
            }

            self.pop(*draw);
            cov_gains.push(start_cov - cov);
        }

        cov_gains
    }

    #[inline]
    pub fn fetch(&self, index: usize) -> f64 {
        self.nodes[index].data
    }

    #[inline]
    pub fn boundaries(&self) -> ((usize, f64), (usize, f64)) {
        (
            (self.left, self.nodes[self.left].data),
            (self.right, self.nodes[self.right].data),
        )
    }

    #[inline]
    pub fn crawl_left(&self, index: usize) -> GLVCrawler<T> {
        GLVCrawler::new(self, index)
    }

    #[inline]
    pub fn crawl_right(&self, index: usize) -> GRVCrawler<T> {
        GRVCrawler::new(self, index)
    }

    pub fn check_integrity(&self) {
        if (self.mad() - slow_mad(&self.ordered_values())).abs() > 0.00001 {
            println!("{:?}", self.nodes);
            println!("{:?}", self.ordered_values());
            println!("{:?}", self.mad());
            println!("{:?}", slow_mad(&self.ordered_values()));
            panic!("Mad mismatch");
        }
    }
}

impl RankVector<Vec<Node>> {
    pub fn derive(&self, indices: &[usize]) -> RankVector<Vec<Node>> {
        let stencil = Stencil::from_slice(indices);
        self.derive_stencil(&stencil)
    }

    #[inline]
    pub fn derive_stencil(&self, stencil: &Stencil) -> RankVector<Vec<Node>> {
        let mut new_nodes: Vec<Node> = vec![Node::blank(); stencil.len() + self.offset];
        let filtered_rank_order: Vec<usize> = self
            .rank_order
            .as_ref()
            .unwrap_or(&vec![])
            .iter()
            .cloned()
            .filter(|x| stencil.frequency.contains_key(x))
            .collect();

        let mut rank_range: HashMap<usize, usize> = filtered_rank_order
            .iter()
            .scan(0, |acc, x| {
                let prev = *acc;
                *acc = *acc + stencil.frequency[x];
                Some((*x, prev))
            })
            .collect();

        let mut new_rank_order = vec![0; stencil.len()];

        for (new_index, old_index) in stencil.indices.iter().enumerate() {
            new_rank_order[rank_range[old_index]] = new_index;
            rank_range.entry(*old_index).and_modify(|x| *x += 1);
        }

        let left = new_nodes.len() - 2;
        let right = new_nodes.len() - 1;

        new_nodes[left] = Node {
            data: 0.,
            index: left,
            rank: 0,
            previous: left,
            next: right,
            zone: 0,
        };

        new_nodes[right] = Node {
            data: 0.,
            index: right,
            rank: 0,
            previous: left,
            next: right,
            zone: 0,
        };

        let mut new_zones = [0; 4];
        let mut new_sums = [0.; 2];
        let mut new_squared_sums = [0.; 2];

        let mut previous = left;

        for (rank, &new_index) in new_rank_order.iter().enumerate() {
            let old_index = stencil.indices[new_index];

            let data = self.nodes[old_index].data;

            let new_node = Node {
                data: data,
                index: new_index,
                rank: rank,
                previous: previous,
                next: right,
                zone: 2,
            };

            new_nodes[previous].next = new_index;
            new_nodes[new_index] = new_node;
            new_zones[2] += 1;
            new_sums[1] += data;
            new_squared_sums[1] += data;

            previous = new_index;
        }

        new_nodes[right].previous = previous;

        let left = *new_rank_order.get(0).unwrap_or(&0);
        let right = *new_rank_order.last().unwrap_or(&0);

        let mut new_vector = RankVector {
            rank_order: Some(new_rank_order),
            zones: new_zones,
            sums: new_sums,
            squared_sums: new_squared_sums,
            offset: self.offset,
            median: (4, 4),
            nodes: new_nodes,
            left: left,
            right: right,
        };

        new_vector.establish_median();
        new_vector.establish_zones();

        new_vector
    }

    #[inline]
    pub fn clone_to_container(
        &self,
        mut local_node_vector: SmallVec<[Node; 1024]>,
    ) -> RankVector<SmallVec<[Node; 1024]>> {
        local_node_vector.clear();

        local_node_vector.reserve(self.nodes.len());

        for node in &self.nodes {
            local_node_vector.push(*node);
        }

        let new_vector = RankVector {
            nodes: local_node_vector,
            rank_order: None,
            zones: self.zones,
            sums: self.sums,
            squared_sums: self.squared_sums,
            offset: self.offset,
            median: self.median,
            left: self.left,
            right: self.right,
        };

        new_vector
    }
}

impl Debug for RankVector<Vec<Node>> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        write!(
            f,
            "RankVec {:?},{:?}",
            self.full_values().cloned().collect::<Vec<f64>>(),
            self.rank_order
        )
    }
}

impl RankVector<SmallVec<[Node; 1024]>> {
    pub fn return_container(self) -> SmallVec<[Node; 1024]> {
        self.nodes
    }

    pub fn empty_sv() -> RankVector<SmallVec<[Node; 1024]>> {
        let container = SmallVec::new();

        let empty = RankVector::<Vec<Node>>::link(&vec![]);

        let mut output = empty.clone_to_container(container);

        output.nodes.grow(1024);

        output
    }

    #[inline]
    pub fn clone_from_prototype(&mut self, prototype: &RankVector<Vec<Node>>) {
        self.nodes.clear();

        for node in &prototype.nodes {
            self.nodes.push(node.clone());
        }

        self.zones = prototype.zones.clone();
        self.sums = prototype.sums;
        self.squared_sums = prototype.squared_sums;
        self.offset = prototype.offset;
        self.median = prototype.median;
        self.left = prototype.left;
        self.right = prototype.right;
    }
}

impl<
        'a,
        T: Borrow<[Node]>
            + BorrowMut<[Node]>
            + Index<usize, Output = Node>
            + IndexMut<usize, Output = Node>
            + Clone
            + Debug,
    > GRVCrawler<'a, T>
{
    #[inline]
    fn new(input: &'a RankVector<T>, first: usize) -> GRVCrawler<'a, T> {
        GRVCrawler {
            vector: input,
            index: first,
        }
    }
}

impl<
        'a,
        T: Borrow<[Node]>
            + BorrowMut<[Node]>
            + Index<usize, Output = Node>
            + IndexMut<usize, Output = Node>
            + Clone
            + Debug,
    > Iterator for GRVCrawler<'a, T>
{
    type Item = usize;

    #[inline]
    fn next(&mut self) -> Option<usize> {
        let Node {
            next,
            index,
            ..
        } = self.vector.nodes[self.index];
        self.index = next;
        return Some(index);
    }
}

#[derive(Clone, Debug)]
pub struct Stencil<'a> {
    frequency: HashMap<usize, usize>,
    indices: &'a [usize],
}

impl<'a> Stencil<'a> {
    pub fn from_slice(slice: &'a [usize]) -> Stencil<'a> {
        let set: HashSet<usize> = slice.iter().cloned().collect();
        let mut frequency: HashMap<usize, usize> = set.iter().map(|x| (*x, 0)).collect();
        for &i in slice.iter() {
            frequency.entry(i).and_modify(|x| *x += 1);
        }
        Stencil {
            frequency: frequency,
            indices: slice,
        }
    }

    pub fn len(&self) -> usize {
        self.indices.len()
    }

    pub fn unique_len(&self) -> usize {
        self.frequency.len()
    }
}

pub struct GRVCrawler<
    'a,
    T: 'a
        + Borrow<[Node]>
        + BorrowMut<[Node]>
        + Index<usize, Output = Node>
        + IndexMut<usize, Output = Node>
        + Clone
        + Debug,
> {
    vector: &'a RankVector<T>,
    index: usize,
}

impl<
        'a,
        T: Borrow<[Node]>
            + BorrowMut<[Node]>
            + Index<usize, Output = Node>
            + IndexMut<usize, Output = Node>
            + Clone
            + Debug,
    > GLVCrawler<'a, T>
{
    #[inline]
    fn new(input: &'a RankVector<T>, first: usize) -> GLVCrawler<'a, T> {
        GLVCrawler {
            vector: input,
            index: first,
        }
    }
}

impl<
        'a,
        T: Borrow<[Node]>
            + BorrowMut<[Node]>
            + Index<usize, Output = Node>
            + IndexMut<usize, Output = Node>
            + Clone
            + Debug,
    > Iterator for GLVCrawler<'a, T>
{
    type Item = usize;

    #[inline]
    fn next(&mut self) -> Option<usize> {
        let Node {
            previous, index, ..
        } = self.vector.nodes[self.index];
        self.index = previous;
        return Some(index);
    }
}

pub struct GLVCrawler<
    'a,
    T: 'a
        + Borrow<[Node]>
        + BorrowMut<[Node]>
        + Index<usize, Output = Node>
        + IndexMut<usize, Output = Node>
        + Clone
        + Debug,
> {
    vector: &'a RankVector<T>,
    index: usize,
}

#[cfg(test)]
mod rank_vector_tests {

    use super::*;
    use crate::utils::test_utils::{slow_median, slow_sme, slow_ssme};

    #[test]
    fn rank_vector_create_empty() {
        let vector = RankVector::<Vec<Node>>::empty();
        vector.ordered_values();
    }

    #[test]
    fn rank_vector_create_trivial() {
        let _vector = RankVector::<Vec<Node>>::link(&vec![]);
    }

    #[test]
    fn rank_vector_create_simple() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        println!("{:?}", vector);
        assert_eq!(
            vector.ordered_values(),
            vec![-3., -2., -1., 0., 5., 10., 15., 20.]
        );
        assert_eq!(vector.median(), slow_median(vector.ordered_values()));
        assert_eq!(slow_mad(&vector.ordered_values()), vector.mad());
    }

    #[test]
    fn rank_vector_create_repetitive() {
        let vector =
            RankVector::<Vec<Node>>::link(&vec![0., 0., -5., -5., -5., 10., 10., 10., 10., 10.]);
        println!("{:?}", vector);
        assert_eq!(
            vector.ordered_values(),
            vec![-5., -5., -5., 0., 0., 10., 10., 10., 10., 10.]
        );
        assert_eq!(vector.median(), 5.);
        assert_eq!(vector.mad(), 5.);
    }

    #[test]
    fn rank_vector_test_sums() {
        let mut vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        println!("{:?}", vector);
        for i in 0..8 {
            println!("Popping {}", i);

            // let output = vector.mpop(i);
            let output = vector.pop(i);
            println!("Got {},{:?}", i, output);

            println!("{:?}", vector.sums);
            println!("{:?}", vector.squared_sums);

            let ordered_value_sum: f64 = vector.ordered_values().iter().sum();
            let computed_sum = vector.sum();

            println!("{:?} vs {:?}", ordered_value_sum, computed_sum);
            assert!(ordered_value_sum - computed_sum < 0.00000000001);

            let ordered_value_sum_of_squares: f64 =
                vector.ordered_values().iter().map(|x| x.powi(2)).sum();
            let computed_sum_of_squares = vector.sum_of_squares();

            println!(
                "{:?} vs {:?}",
                ordered_value_sum_of_squares, computed_sum_of_squares
            );
            assert!(ordered_value_sum_of_squares - computed_sum_of_squares < 0.00000000001);
        }
    }

    #[test]
    fn rank_vector_sequential_mad_simple() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        let mut vm = vector.clone();

        for draw in vector.draw_order() {
            println!("{:?}", vm.ordered_values());
            println!(
                "Median:{},{}",
                vm.median(),
                slow_median(vm.ordered_values())
            );
            println!("MAD:{},{}", vm.mad(), slow_mad(&vm.ordered_values()));
            println!("Boundaries:{:?}", vm.boundaries());
            println!("{:?}", vm.pop(draw));
            println!("{:?}", vm.ordered_values());
            println!(
                "Median:{},{}",
                vm.median(),
                slow_median(vm.ordered_values())
            );
            println!("MAD:{},{}", vm.mad(), slow_mad(&vm.ordered_values()));
            println!("Boundaries:{:?}", vm.boundaries());
            assert_eq!(vm.median(), slow_median(vm.ordered_values()));
            assert_eq!(vm.mad(), slow_mad(&vm.ordered_values()));
        }
    }

    #[test]
    fn rank_vector_sequential_var_simple() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);

        let mut vm = vector.clone();

        for draw in vector.draw_order() {
            println!("{:?}", vm.ordered_values());
            println!(
                "Median:{},{}",
                vm.median(),
                slow_median(vm.ordered_values())
            );
            println!("MAD:{},{}", vm.mad(), slow_mad(&vm.ordered_values()));
            println!("Boundaries:{:?}", vm.boundaries());
            println!("{:?}", vm.pop(draw));
            println!("{:?}", vm.ordered_values());
            println!(
                "Median:{},{}",
                vm.median(),
                slow_median(vm.ordered_values())
            );
            println!("MAD:{},{}", vm.mad(), slow_mad(&vm.ordered_values()));
            println!("Boundaries:{:?}", vm.boundaries());
            assert_eq!(vm.median(), slow_median(vm.ordered_values()));
            assert_eq!(vm.mad(), slow_mad(&vm.ordered_values()));
        }
    }

    #[test]
    fn rank_vector_sequential_sme_simple() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        let draw_order = vector.draw_order();
        let mut vm = vector.clone();
        let ordered_sme = vector.clone().ordered_sme(&draw_order);
        println!("{:?}", ordered_sme);
        let mut slow_ordered_sme = vec![];
        for draw in vm.draw_order() {
            println!("{:?}", vm.ordered_values());
            println!("{:?}", slow_sme(vm.ordered_values()));
            slow_ordered_sme.push(slow_sme(vm.ordered_values()));
            vm.pop(draw);
        }
        assert_eq!(ordered_sme, slow_ordered_sme);
    }

    #[test]
    fn rank_vector_sequential_ssme_simple() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        let draw_order = vector.draw_order();
        let mut vm = vector.clone();
        let ordered_ssme = vector.clone().ordered_ssme(&draw_order);
        println!("{:?}", ordered_ssme);
        let mut slow_ordered_ssme = vec![];
        for draw in vm.draw_order() {
            println!("{:?}", vm.ordered_values());
            println!("{:?}", slow_ssme(vm.ordered_values()));
            slow_ordered_ssme.push(slow_ssme(vm.ordered_values()));
            vm.pop(draw);
        }
        assert_eq!(ordered_ssme, slow_ordered_ssme);
    }

    #[test]
    fn rank_vector_derive_test() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        let kid1 = vector.derive(&vec![0, 3, 6, 7]);
        let kid2 = vector.derive(&vec![1, 4, 5]);
        eprintln!("{:?}", kid1);
        assert_eq!(kid1.median(), 12.5);
        assert_eq!(kid2.median(), -2.);
        assert_eq!(kid1.ssme(), 125.);
        assert_eq!(kid1.var(), 31.25);
        assert_eq!(kid1.rank_order, Some(vec![1, 0, 2, 3]));
    }

    #[test]
    fn rank_vector_derive_double() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        let kid1 = vector.derive(&vec![0, 0, 3, 3, 6, 7]);
        let kid2 = vector.derive(&vec![1, 4, 5]);
        eprintln!("{:?}", kid1);
        assert_eq!(kid1.median(), 10.);
        assert_eq!(kid2.median(), -2.);
        assert_eq!(kid1.ssme(), 175.);
        assert!((kid1.var() - 28.472222222).abs() < 0.0001);
        assert_eq!(kid1.rank_order, Some(vec![2, 3, 0, 1, 4, 5]));
    }
    // 10,10,5,5,15,20
    // 5,5,10,10,15,20

    #[test]
    fn rank_vector_fetch_test() {
        let vector = RankVector::<Vec<Node>>::link(&vec![10., -3., 0., 5., -2., -1., 15., 20.]);
        assert_eq!(vector.fetch(0), 10.);
        assert_eq!(vector.fetch(1), -3.);
        assert_eq!(vector.fetch(2), 0.);
        assert_eq!(vector.fetch(3), 5.);
    }
}
