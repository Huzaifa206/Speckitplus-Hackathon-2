'use client';

import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from '@/components/ui/select';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Search, Filter, ArrowUpDown } from 'lucide-react';
import { useState } from 'react';

interface FiltersProps {
  onSearchChange: (search: string) => void;
  onPriorityChange: (priority: string) => void;
  onSortChange: (sort: string) => void;
}

export function Filters({ onSearchChange, onPriorityChange, onSortChange }: FiltersProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedPriority, setSelectedPriority] = useState('all');
  const [selectedSort, setSelectedSort] = useState('created_at');

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setSearchTerm(value);
    onSearchChange(value);
  };

  const handlePriorityChange = (value: string) => {
    setSelectedPriority(value);
    onPriorityChange(value);
  };

  const handleSortChange = (value: string) => {
    setSelectedSort(value);
    onSortChange(value);
  };

  return (
    <div className="flex flex-col md:flex-row gap-4 mb-6 p-4 bg-muted/50 rounded-lg">
      <div className="relative flex-1">
        <Search className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Search tasks..."
          value={searchTerm}
          onChange={handleSearch}
          className="pl-8"
        />
      </div>

      <div className="flex gap-2">
        <div className="relative">
          <Filter className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Select value={selectedPriority} onValueChange={handlePriorityChange}>
            <SelectTrigger className="pl-8 w-[180px]">
              <SelectValue placeholder="Priority" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="all">All Priorities</SelectItem>
              <SelectItem value="high">High</SelectItem>
              <SelectItem value="medium">Medium</SelectItem>
              <SelectItem value="low">Low</SelectItem>
            </SelectContent>
          </Select>
        </div>

        <div className="relative">
          <ArrowUpDown className="absolute left-2 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
          <Select value={selectedSort} onValueChange={handleSortChange}>
            <SelectTrigger className="pl-8 w-[180px]">
              <SelectValue placeholder="Sort by" />
            </SelectTrigger>
            <SelectContent>
              <SelectItem value="created_at">Date Created</SelectItem>
              <SelectItem value="due_date">Due Date</SelectItem>
              <SelectItem value="priority">Priority</SelectItem>
              <SelectItem value="title">Title</SelectItem>
            </SelectContent>
          </Select>
        </div>
      </div>
    </div>
  );
}